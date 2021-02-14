import csv
import re
from stimulus_info import stimulus_info

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
            with open(file) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                prev_emotion_id = ""
                is_practice = False
                photo_num = 0
                new_rows = []

                for row in reader:
                    curr_emotion, emotion_id, percent = self.__convert_filename_to_emotion_and_id(row['stimFile'])
                    new_row['Latency'] += self.image_presentation_time
                    new_row['Percent Emotion'] = percent

                    if emotion_id != "" and (prev_emotion_id == "" or emotion_id != prev_emotion_id):
                        # we entered a new trial
                        prev_emotion_id = emotion_id
                        new_row = self.__init_new_row()
                        new_row['ID'] = emotion_id
                        new_row['Stimulus Emotion'] = curr_emotion
                        new_row['Stimulus Gender'] = self.__determine_gender(curr_emotion)
                        new_row['Stimulus Ethnicity'] = self.__determine_ethnicity(emotion_id)
                        photo_num = 1


                    if row['space_pressed_practice.rt'] is not None:
                        is_practice = True
                        new_row['Latency'] += row['space_pressed_practice.rt']
                    elif row['space_pressed.rt'] is not None:
                        new_row['Latency'] += row['space_pressed.rt']
                    elif row['space_pressed_2.rt'] is not None:
                        new_row['Latency'] += row['space_pressed_2.rt']

                    if row['key_resp.keys'] is not None and row['key_resp.rt'] is not None:
                        new_row['Latency'] += row['key_resp.rt']
                        new_row['Response'] = row['key_resp.keys']
                        new_row['Accuracy'] = self.__determine_accuracy(curr_emotion, row['key_resp.keys'])
                        new_row['Photonum'] = photo_num
                        new_rows.append(new_row)


                    photo_num += 1

    def __init_new_row(self):
        return {'Participant': "", 'trial': "", 'ID': "", 'Stimulus Gender': "",
                'Stimulus Ethnicity': "", 'Stimulus Emotion': "", 'Response': 0, 'Latency': 0, 'Percent Emotion': -1, 'Photonum': -1}


    def __convert_filename_to_emotion_and_id(self, filename):
        if filename is None:
            return "", ""
        else:
            emotion_file_path = filename.split("/")[-1].split(".")[0]
            emotion_id = emotion_file_path.split("_")[0]
            emotion = emotion_file_path.split("_")[1]
            percent = emotion_file_path.split("_")[-1]
            return emotion, emotion_id, percent

    def __determine_gender(self, emotion_id):
        return stimulus_info[emotion_id]['gender']

    def __determine_ethnicity(self, emotion_id):
        return stimulus_info[emotion_id]['ethnicity']

    def __determine_accuracy(self, curr_emotion, response):
        if curr_emotion == 'AN' and response == 1:
            return 1
        elif curr_emotion == 'FE' and response == 2:
            return 1
        elif curr_emotion == 'HA' and response == 3:
            return 1
        elif curr_emotion == 'SA' and response == 4:
            return 1
        else:
            return 0

    def __process_file(self):
        results = []

        return results

    def __construct_new_csv(self, file):
        with open(file.split('.')[0] + '-processed.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')


    def __write_new_rows(new_rows, file):
        new_file_name = file + '-processed'
        with open(file + '-processed', 'w') as csv_file:
            writer = csv.DictWriter(new_file_name, fieldnames=self.headers)
            writer.writeheader()

            for row in new_rows:
                writer.writerow(row)
