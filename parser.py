import csv
import re

class Parser:

    # trial = P1, P2, 1 ...
    # ID = 01F
    def __init__(self, files):
        self.files = files
        self.headers= ['Participant', 'trial', 'ID',
                       'Stimulus Gender', 'Stimulus Ethnicity', 'Stimulus Emotion',
                       'Response', 'Accuracy', 'Latency', 'Percent Emotion', 'Photonum']
        self.image_presentation_time = 0.1

    def parse(self):
        self.__read_files()

    def __read_files(self):
        for file in self.files:
            with open(file, newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                prev_emotion_id = ""
                latency = 0
                is_practice = False
                gender = ""
                for row in reader:
                    curr_emotion, emotion_id = self.__convert_filename_to_emotion_and_id(row['stimFile'])
                    latency += self.image_presentation_time

                    if prev_emotion_id != "" and emotion_id != "" and emotion_id != prev_emotion_id:
                        # we entered a new trial
                        prev_emotion_id = emotion_id
                        gender = self.__determine_gender(curr_emotion)

                    if row['space_pressed_practice.rt'] is not None:
                        is_practice = True
                        latency += row['space_pressed_practice.rt']
                    elif row['space_pressed.rt'] is not None:
                        latency += row['space_pressed.rt']


    def __convert_filename_to_emotion_and_id(self, filename):
        if filename is None:
            return "", ""
        else:
            emotion_name = filename.split("/")[-1].split(".")[0]
            emotion_id = emotion_name.split("_")[0]
            emotion = emotion_name.split("_")[1]
            return emotion, emotion_id

    def __determine_gender(self, emotion):
        match = re.search("[M,F]", emotion)

        if match is None or len(match.group()) > 1:
            return ""
        else:
            return match.group()


    def __process_file(self):
        results = []

        return results



    def __construct_new_csv(self, file):
        with open(file.split('.')[0] + '-processed.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')



