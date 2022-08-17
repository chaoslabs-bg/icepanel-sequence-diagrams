# IcePanel Flow to Mermaid Sequence

This is a CLI tool that converts [IcePanel](https://icepanel.io/) flow and output to [Mermaid](https://mermaid-js.github.io/mermaid/#/) sequence diagram. 
It also contains a docker image should one require to create the sequence and get it rendered to supported format.

## Usage

### Install

To install locally, run:

```shell
git clone https://github.com/chaoslabs-bg/icepanel-sequence-diagrams.git
cd icepanel-sequence-diagrams
# Optional ####
# create virtual environment
python3 -m venv venv
# /Optional ####
pip install -r requirements.txt
```

### Standalone

```shell
export API_KEY=<your-icepanel-api-key>
export LANDSCAPE_ID=<your-landscape-id>
export MMDC_CMD=/path/to/mmdc #optional only if you want to convert the .mmd to .png
python main.py --flow-name="Name of my flow"
```

### Docker

[Docker Hub link](https://hub.docker.com/r/cladmin/icepanel_mermaid_sequence)

```shell
```shell
docker pull cladmin/icepanel_mermaid_sequence 
docker run -it --env LANDSCAPE_ID="<your_landscape_id>" --env API_KEY="<your_ice_panel_api_key>" -v $(PWD)/data:/app/data docker.io/cladmin/icepanel_mermaid_sequence:v1 --flow-name="My First Flow" --convert
```
