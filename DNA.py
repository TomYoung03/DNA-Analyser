
class DNA:
    '''
    class used to store DNA information
    '''
    def __init__(self,sequence,RNA = False):

        self.bases_list = ["a", "t", "c", "g"]
        self.reverse_dict = {"a": "t",
                             "t": "a",
                             "c": "g",
                             "g": "c"}

        self.raw_sequence = sequence.lower().replace(" ","").replace("u","t")
        self.validate(self.raw_sequence)
        self.formatted_sequence = self.arrange(self.raw_sequence)
        self.reverse_comp_sequence = self.reverse_comp(self.raw_sequence)

        self.length = len(self.raw_sequence)
        self.A_count = self.raw_sequence.count("a")
        self.T_count = self.raw_sequence.count("t")
        self.C_count = self.raw_sequence.count("c")
        self.G_count = self.raw_sequence.count("g")

        self.num_AT,self.num_CG = self.get_base_content()
        self.per_AT,self.per_CG = self.get_base_content(percent =True)

    def validate(self,sequence):

        for base in list(sequence):
            if base not in self.bases_list:
                raise Exception("Incorrect base")

    def arrange(self,sequence):
        seq_list = list(sequence)
        new_seq = []
        location = 0
        for i in seq_list:
            if location != 0 and location % 3 == 0:
                new_seq.append(" ")
                new_seq.append(i)
            else:
                new_seq.append(i)
            location += 1
        return "".join(new_seq)

    def get_base_content(self, percent = False):
        '''
        :param percent: if true then returns percentages if false then only returns as a count
        :return: count or percent of AT,CG content
        '''
        if not percent:
            return self.A_count+self.T_count, self.C_count+self.G_count
        if percent:
            return round((self.num_AT/self.length)*100), \
                   round((self.num_CG/self.length)*100)

    def print(self,formatted = False):
        if not formatted:
            return self.raw_sequence
        if formatted:
            return self.formatted_sequence

    def sequence_search(self, sequence):
        '''
        returns a DNA string with the sequence in upper case
        :param sequence: Sequence to be looked for
        :return: formatted DNA
        '''
        #converted to str allows it to work with argument that is DNA class
        sequence = str(sequence)
        searched_DNA = self.raw_sequence
        if sequence in self.raw_sequence:
            searched_DNA = searched_DNA.replace(sequence, sequence.upper())
            return searched_DNA
        else:
            return False

    def reverse_comp(self,sequence):
        new_seq = []
        sequence = list(sequence)
        for base in reversed(sequence):
            new_seq.append(self.reverse_dict[base])
        return "".join(new_seq)

    def full_info(self):

        info = ("Raw sequence: " + self.raw_sequence + "\n\nBase count:"
                   + "\nA: "+ str(self.A_count) + " T: " + str(self.T_count) + " C: "+ str(self.C_count) + " G: "+ str(self.G_count)
                   +"\n\nAT percentage: " + str(self.per_AT) + "% CG percentage: " + str(self.per_CG) +"%"
                   +"\n\nFormatted sequence: " + self.formatted_sequence
                   )
        return info



    def __str__(self):
        return self.raw_sequence


