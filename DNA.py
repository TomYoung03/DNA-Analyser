
class DNA:
    '''
    class used to store DNA information
    '''
    def __init__(self,sequence,RNA = False):

        self.RNA = RNA
        self.bases_list = ["a", "t", "c", "g"] if RNA == False else ["a","u","c","g"]
        self.reverse_dict = {"a": "t",
                             "t": "a",
                             "c": "g",
                             "g": "c"} if RNA == False else {"a": "u",
                                                            "u": "a",
                                                            "c": "g",
                                                            "g": "c"}
        self.DNA_prot_dictionary = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': 'STOP', 'TAG': 'STOP',
            'TGC': 'C', 'TGT': 'C', 'TGA': 'STOP', 'TGG': 'W',
        }

        self.raw_sequence = sequence.lower().replace(" ","").rstrip()
        self.validate(self.raw_sequence)
        self.formatted_sequence = self.arrange(self.raw_sequence)
        self.reverse_comp_sequence = self.reverse_comp(self.raw_sequence)

        self.length = len(self.raw_sequence)
        self.A_count = self.raw_sequence.count("a")
        self.T_count = self.raw_sequence.count("t") if RNA == False else self.raw_sequence.count("u")
        self.C_count = self.raw_sequence.count("c")
        self.G_count = self.raw_sequence.count("g")

        self.num_AT,self.num_CG = self.get_base_content()
        self.per_AT,self.per_CG = self.get_base_content(percent =True)

    def validate(self,sequence):

        for base in list(sequence):
            if base not in self.bases_list:
                raise DNA_exceptions("Incorrect base: " + base +" in sequence")

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

        #RNA info has T references modified to U
        DNA_info = ("Raw sequence: " + self.raw_sequence + "\n\nBase count:"
                   + "\nA: "+ str(self.A_count) + " T: " + str(self.T_count) + " C: "+ str(self.C_count) + " G: "+ str(self.G_count)
                   +"\n\nAT percentage: " + str(self.per_AT) + "% CG percentage: " + str(self.per_CG) +"%"
                   +"\n\nFormatted sequence: " + self.formatted_sequence
                   )
        RNA_info = ("Raw sequence: " + self.raw_sequence + "\n\nBase count:"
                   + "\nA: "+ str(self.A_count) + " U: " + str(self.T_count) + " C: "+ str(self.C_count) + " G: "+ str(self.G_count)
                   +"\n\nAU percentage: " + str(self.per_AT) + "% CG percentage: " + str(self.per_CG) +"%"
                   +"\n\nFormatted sequence: " + self.formatted_sequence
                   )
        info = DNA_info if self.RNA == False else RNA_info
        return info

    def convert_RNA(self):

        if not self.RNA:
            RNA_seq = [ base if base != "t" else "u" for base in self.raw_sequence ]
            return "".join(RNA_seq)
        else:
            return self.raw_sequence

    def translate(self):
        prot_seq = []
        #loop goes through range increasing by 3 each time
        for i in range(0,len(self.raw_sequence),3):
            try:
                codon = self.raw_sequence[i:i+3].replace("u","t").upper()
                prot_seq.append(self.DNA_prot_dictionary[codon])
            except:
                #deals with sequence that dont perfectly divide by 3
                pass
        return " ".join(prot_seq)


    def modify(self,new_amino_acid,location):

        try:
            #looks at codon location and finds amino acid via dict
            current_amino_acid = self.DNA_prot_dictionary[self.raw_sequence[location:location+3].upper()]
            #codon to be changed
            current_codon = self.raw_sequence[location:location+3]
            #creates a list of the keys (codons) for amino acids matching the one given in new_amino_acid
            new_codons_list = [key for key,value in self.DNA_prot_dictionary.items() if value == new_amino_acid.upper()]
        except:
            #can have errors if e.g location + 3 is out of index
            return False

        if new_amino_acid == current_amino_acid:
            print("Amino acid " + new_amino_acid + "is already at codon " + current_codon)
        else:
            #output eventuall contains all information needed
            output = ["Your options are:",]
            for codon in new_codons_list:
                output.append(current_codon + " ----> " + codon)
                #loop adds the new codon to the sequence letter by letter in upercase
                # need to reset sequence to original every loop
                sequence = list(self.raw_sequence)
                for i in range(0,3):
                    sequence[location+i] = list(codon)[i].upper()
                output.append("Sequence: " + "".join(sequence))

            return "\n".join(output)





    def __str__(self):
        #when used a string returns the raw original sequence
        return self.raw_sequence
    def __len__(self):
        return len(self.raw_sequence)



class DNA_exceptions(Exception):

     def __init__(self,message):
         super(DNA_exceptions,self).__init__(message)
         self.message = message
