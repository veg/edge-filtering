from Bio import SeqIO

def remove_spaces(input, output):
    for i in range(len(input)):
        sequences = SeqIO.parse(input[i], "fasta")
        with open(output[i], "w") as output_handle:
            SeqIO.write(sequences, output_handle, "fasta")

    return
