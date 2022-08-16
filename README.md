# IcePanel Flow to Mermaid Sequence

This is a CLI tool that converts [IcePanel](https://icepanel.io/) flow and output to [Mermaid](https://mermaid-js.github.io/mermaid/#/) sequence diagram. 
It also contains a docker image should one require to create the sequence and get it rendered to supported format.

## Usage

```bash
export API_KEY=<your-icepanel-api-key>
export LANDSCAPE_ID=<your-landscape-id>
export MMDC_CMD=/path/to/mmdc #optional only if you want to convert the .mmd to .png
python main.py --flow-name="Name of my flow"
```
