import csv
import re
import os
from stimulus_info import stimulus_info

class Parser:

    # trial = P1, P2, 1 ...
    # ID = 01F
    def __init__(self, files):
        self.files = files
        self.headers= ['Participant', 'trial', 'ID',
                       'Stimulus Gender', 'Stimulus Ethnicity', 'Stimulus Emotion',
                       'Response', 'Accuracy', 'Latency', 'Percent Emotion', 'Photonum']
        self.image_presentation_time = 0.25

    def parse(self):
        self.__read_files()

    def __read_files(self):
        for file in self.files:
            with open(file) as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                new_rows = []
                new_row = self.__init_new_row()
                practice_trial_count = 1
                trial_count = 1

                for row in reader:

                    if row['space_pressed_practice.rt'] != '':
                        new_row['Latency'] += float(row['space_pressed_practice.rt'])
                        new_row['trial'] = "P" + str(practice_trial_count)
                        practice_trial_count += 1
                        self.__write_new_row_meta(row, new_row)
                    elif row['space_pressed.rt'] != '':
                        new_row['Latency'] += float(row['space_pressed.rt'])
                        new_row['trial'] = trial_count
                        trial_count += 1
                        self.__write_new_row_meta(row, new_row)
                    elif row['space_pressed_2.rt'] != '':
                        new_row['Latency'] += float(row['space_pressed_2.rt'])
                        new_row['trial'] = trial_count
                        trial_count += 1
                        self.__write_new_row_meta(row, new_row)
                    elif row['key_resp.keys'] != '' and row['key_resp.rt'] != '':
                        new_row['Latency'] += float(row['key_resp.rt'])
                        new_row['Response'] = row['key_resp.keys']
                        new_row['Accuracy'] = self.__determine_accuracy(new_row['Stimulus Emotion'], row['key_resp.keys'])
                        new_row['Participant'] = row['participant']
                        new_rows.append(new_row)
                        new_row = self.__init_new_row()
                    else:
                        new_row['Latency'] += self.image_presentation_time
                        new_row['Photonum'] += 1

            self.__write_new_rows(new_rows, file)

    def __init_new_row(self):
        return {'Participant': "", 'trial': "", 'ID': "", 'Stimulus Gender': "",
                'Stimulus Ethnicity': "", 'Stimulus Emotion': "", 'Response': 0, 'Latency': 0, 'Percent Emotion': 0, 'Photonum': 0}

    def __write_new_row_meta(self, row, new_row):
        curr_emotion, emotion_id, percent = self.__convert_filename_to_emotion_and_id(row['stimFile'])
        new_row['Percent Emotion'] = percent
        new_row['ID'] = emotion_id
        new_row['Stimulus Emotion'] = curr_emotion
        new_row['Stimulus Gender'] = self.__determine_gender(emotion_id)
        new_row['Stimulus Ethnicity'] = self.__determine_ethnicity(emotion_id)

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
        if curr_emotion == 'AN' and response == '1':
            return 1
        elif curr_emotion == 'FE' and response == '2':
            return 1
        elif curr_emotion == 'HA' and response == '3':
            return 1
        elif curr_emotion == 'SA' and response == '4':
            return 1
        else:
            return 0

    def __process_file(self):
        results = []

        return results

    def __write_new_rows(self, new_rows, file):
        dir = self.__create_processed_dir(file)
        processed_file_name = os.path.basename(file).split('.')[0] + '-processed.csv'
        new_file_name = os.path.join(dir, processed_file_name)

        with open(new_file_name, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()

            for row in new_rows:
                writer.writerow(row)

    def __create_processed_dir(self, file):
        dir = os.path.join(os.path.dirname(file), 'processed')
        try:
            os.makedirs(dir)
        except FileExistsError as e:
            print(e)
            pass

        return dir
