from fastapi import FastAPI
app = FastAPI()

rolles = []

@app.get("/scores")
def input_scores(pins: int):
    rolles.append(pins)

    return {"current_roll" : pins,
            "all_rolles" : rolles}
