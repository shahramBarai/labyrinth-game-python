
class Score():
    def __init__(self):
        self.fileName = "score.txt"
        self.sizes = ["Small", "Normal", "Big"]
        self.score = []
        self.read_from_file()
        
    def get_score_list(self):
        return self.score
    
    def read_from_file(self):
        try:
            file = open(self.fileName, "r")
            for line in file:
                line = line.rstrip()
                self.score.append(self.convert_to_score_list(line))
            file.close()
        except OSError:
            print("Error! Something went wrong while reading the {} file!".format(self.fileName))
            
    def write_to_file(self):
        try:
            file = open(self.fileName, "w")
            for x in range(5):
                file.write(self.convert_to_string(self.score[x])+ "\n")
            file.close()
        except OSError:
            print("Error! Something went wrong while writing the {} file!".format(self.fileName))
            
    def convert_to_string(self, score_list):
        line = ""
        if len(score_list) == 0:
            return line
        if score_list[0] in self.sizes:     # When size is string
            line += score_list[0]
        else:                               # when size is (x, y)
            size = score_list[0]
            line = line + str(size[0]) +"x"+ str(size[1])
        for i in range(1, 4):
            line = line + " " + str(score_list[i])
        return line
    
    def convert_to_score_list(self, score_line):
        if score_line == "":
            return []
        score_list = score_line.rsplit(" ")
        if score_list[0] not in self.sizes:
            size = score_list[0].split("x")
            size = (int(size[0]), int(size[1]))
        else: size = score_list[0]
        name = score_list[1]
        score = int(score_list[2])
        time = int(score_list[3])
        return [size, name, score, time]
            
    def compare_score(self, size, name, score, time):
        '''(str, str, int, int)
        or ((int, int), str, int, int)
        '''
        if size in self.sizes:
            line = self.score[self.sizes.index(size)]             # line = [size, name, score, time]
            if len(line) == 0:
                line = [size, name, score, time]
            elif score > line[2]:
                line[1] = name
                line[2] = score
                line[3] = time
            elif score == line[2] and time <= line[3]:
                line[1] = name
                line[2] = score
                line[3] = time
        else:
            for i in range(3, 5):
                if len(self.score[i]) == 0:
                    self.score[i] = [size, name, score, time]
                    break
                elif (score >= self.score[i][2]):
                    area = self.score[i][0][0] * self.score[i][0][1]
                    if score > self.score[i][2]:
                        self.score[i][0] = size
                        self.score[i][1] = name
                        self.score[i][2] = score
                        self.score[i][3] = time
                        break
                    elif score == self.score[i][2] and (size[0] * size[1]) > area:
                        self.score[i][0] = size
                        self.score[i][1] = name
                        self.score[i][2] = score
                        self.score[i][3] = time
                        break
                    elif score == self.score[i][2] and (size[0] * size[1]) == area and time <= self.score[i][3]:
                        self.score[i][0] = size
                        self.score[i][1] = name
                        self.score[i][2] = score
                        self.score[i][3] = time
                        break