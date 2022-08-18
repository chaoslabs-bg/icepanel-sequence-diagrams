import os
from enum import Enum
from pathlib import Path

import typer
from os import environ

import requests

headers = {"Authorization": f"ApiKey {environ['API_KEY']}"}

landscape_id = environ['LANDSCAPE_ID']
version_id = environ['LANDSCAPE_VERSION']


class MermaidExportType(str, Enum):
    svg = "svg"
    png = "png"


class SequenceParticipant:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"{self.id} - {self.name}"


class SequenceInteraction:
    def __init__(self, id, type, description, source_id, target_id):
        self.id = id
        self.type = type
        self.description = description
        self.source_id = source_id
        self.target_id = target_id

    def __str__(self):
        return f"{self.id} - {self.type} - {self.description} - {self.source_id} - {self.target_id}"


class MermaidSequence:

    def __init__(self, name):
        self.name = name
        self.participants = {}
        self.sequence_steps = []

    def add_participant(self, participant: SequenceParticipant):
        if participant.id not in self.participants:
            self.participants[participant.id] = participant

    def add_sequence_step(self, sequence_step: SequenceInteraction):
        self.sequence_steps.append(sequence_step)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def generate(self):
        graph_data = "sequenceDiagram\n"
        graph_data += f"\tautonumber\n"
        for participant in self.participants.values():
            graph_data += f"\tparticipant {participant.id} as {participant.name}\n"
        for sequence_step in self.sequence_steps:
            if sequence_step.target_id is None:
                graph_data += f"\t{sequence_step.source_id} -->> {sequence_step.source_id}: {sequence_step.description}\n"
            else:
                graph_data += f"\t{sequence_step.source_id} ->> {sequence_step.target_id}: {sequence_step.description}\n"
        return graph_data


model_objects = {}
diagrams = {}


def get_model_object(model_object_id):
    if model_object_id in model_objects:
        return model_objects[model_object_id]
    rmodel = requests.get(
        f"https://api.icepanel.io/v1/landscapes/{landscape_id}/versions/{version_id}/model/objects/{model_object_id}",
        headers=headers)
    model_object = rmodel.json()["modelObject"]
    model_objects[model_object_id] = model_object
    return model_object


def get_diagram_object(diagram_id, object_id):
    if object_id in diagrams:
        dia = diagrams[object_id]
    else:
        rdia = requests.get(
            f"https://api.icepanel.io/v1/landscapes/{landscape_id}/versions/{version_id}/diagrams/{diagram_id}",
            headers=headers)
        dia = rdia.json()["diagram"]
        diagrams[object_id] = dia
    print(dia["objects"])
    print(object_id)
    diagram_object = dia["objects"][object_id]
    return diagram_object


def find_flow_by_name(name):
    """
    For given flow name finds its id
    :param name:
    :return:
    """
    rflow = requests.get(
        f"https://api.icepanel.io/v1/landscapes/{landscape_id}/versions/{version_id}/flows",
        headers=headers)

    # {{baseUrl}}/landscapes/:landscapeId/versions/:versionId/flows/:flowId
    flows = rflow.json()["flows"]
    for flow in flows:
        if flow["name"] == name:
            return flow["id"]
    return None


def create_file_name(filename, extension):
    keepcharacters = (' ', '.', '_')
    safe_filename = "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
    return f"{safe_filename}.{extension}"


def main(flow_name: str = typer.Option("The name of the flow to create sequence diagram for"),
         export_type: MermaidExportType = MermaidExportType.png,
         convert: bool = typer.Option(False, "--convert", "-c",
                                      help="Converts the generated sequence to supported output format. Requires MMDC_CMD environment variable to be set to the path of mermaid executable"),
         data_dir: Path = typer.Option("data/", "--data-dir", "-d",
                                       help="Path where to store the generated sequence diagram"),
         ):
    flow_id = find_flow_by_name(flow_name)
    if flow_id is None:
        # TODO add debug info (e.g. http call info)
        typer.secho(f"Unable to find flow [{flow_name}]", fg=typer.colors.RED)
        return
    rflow = requests.get(
        f"https://api.icepanel.io/v1/landscapes/{landscape_id}/versions/{version_id}/flows/{flow_id}",
        headers=headers)

    # print(rflow.json())
    if rflow.status_code != 200 or "flow" not in rflow.json():
        typer.secho(f"Unable to find flow [{rflow.json()}]", fg=typer.colors.RED)
        return
    flow = rflow.json()["flow"]
    seq = MermaidSequence(flow["name"])
    steps = {k: v for k, v in sorted(flow["steps"].items(), key=lambda item: item[1]["index"])}

    for k, v in steps.items():
        dia_obj_ori = get_diagram_object(flow["diagramId"], v["originId"])
        dia_obj_tar = get_diagram_object(flow["diagramId"], v["targetId"]) if v["targetId"] is not None else None
        model_obj_ori = get_model_object(dia_obj_ori["modelId"])
        model_obj_tar = None
        if dia_obj_tar is not None:
            model_obj_tar = get_model_object(dia_obj_tar["modelId"])
        participant_ori = SequenceParticipant(model_obj_ori["id"], model_obj_ori["name"])
        seq.add_participant(participant_ori)
        participant_tar = None
        if model_obj_tar is not None:
            participant_tar = SequenceParticipant(model_obj_tar["id"], model_obj_tar["name"])
            seq.add_participant(participant_tar)
        interaction = SequenceInteraction(v["id"], v["type"], v["description"], participant_ori.id,
                                          participant_tar.id if participant_tar is not None else None)
        # print(f"{k}: {v['description']} - {v['type']} - {model_obj_ori['name']}")
        seq.add_sequence_step(interaction)
    print(seq.generate())
    f = open(f"./data/{create_file_name(flow_name, 'mmd')}", "w")
    f.write(seq.generate())
    f.close()
    if convert:
        os.system(
            f"{environ['MMDC_CMD']} -p puppeteer-config.json -i \"{data_dir}/{create_file_name(flow_name, 'mmd')}\" -o \"{data_dir}/{create_file_name(flow_name, export_type.value)}\"")  # -b transparent


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    typer.run(main)
