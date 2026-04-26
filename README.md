# Kentucky Stroke Metrics for SEQIP

Dash app with fabricated AHA Get With The Guidelines-Stroke style metrics for a Kentucky SEQIP statewide system of care dashboard.

The dataset is generated in `app.py` and is intentionally synthetic. It should not be used for clinical, regulatory, public performance, or AHA GWTG reporting.

## Run locally

```bash
conda activate spyder-env
pip install -r requirements.txt
python app.py
```

Open the local URL printed by Dash.

## Deploy on Posit Connect Cloud

1. Push this project to a public GitHub repository.
2. In Posit Connect Cloud, choose Publish.
3. Select Dash.
4. Select the public `dash-test` repository and the target branch.
5. Choose `app.py` as the primary file.
6. Publish.

Connect Cloud will install dependencies from `requirements.txt` and serve the Dash application object named `app`.
