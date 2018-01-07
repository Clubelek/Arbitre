from pathlib import Path
import pickle

##########################
# SCORE SAVING FUNCTIONS #
##########################


def _save_scores(scores):
    scores_file = open("scores.bin", "wb")
    pickle.dump(scores, scores_file, pickle.HIGHEST_PROTOCOL)


def _retrieve_scores():
    scores = {}

    if Path("scores.bin").is_file():
        scores_file = open("scores.bin", "rb")
        scores = pickle.load(scores_file)

    return scores