from Bio import SeqIO

def remove_spaces(input, output):
    print(output)

    for i in range(len(input)):

        sequences = list(SeqIO.parse(input[i], "fasta"))

        # clip sequences
        for j in range(len(sequences)):
            sequences[j].id = sequences[j].id.split('_')[0]
            sequences[j].name = sequences[j].name.split('_')[0]

        with open(output[i], "w") as output_handle:
            SeqIO.write(sequences, output_handle, "fasta")

    return
