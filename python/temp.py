import pandas as pd
import argparse
import os

dirname = os.path.dirname(os.path.realpath(__file__))

def matrix_maker(internal, tip, matrix_node_count):
    print('\n         generating the matrix... \n' )
    nodes = list(range(int(matrix_node_count)))
    ## payload for column 1 (node ID) ##
    j = [i +1 for i in nodes]
    print('Total number of  nodes in the network: ' + str(j[-1]) + '\n')

    ## payload for column 2 (source nodes) ##
    nodes[0] = -1

    ## payload for columns 3 ( internal length) and 4 (tip length) ##
    temp_internal = [0.005 for i in nodes]
    temp_tip = [0 for i in nodes]
    #print(len(j), len(nodes), len(temp_internal), len(temp_tip))
    d = {'Node ID': j, 'Source Node': nodes, 'Internal Length': temp_internal, 'Tip Length':temp_tip}
    df = pd.DataFrame(d)
    return df

def matrix_writer(matrix, format):
    print('\n         writing the matrix to a file... \n' )

    number = str(len(matrix))
    filepath =  (os.path.join(dirname, '../data/matrix/'))

    if(format == 'csv'):
        filename =  (os.path.join(filepath, '%s_nodes.csv' % number))
        print(filename)
        matrix.to_csv(filename, sep=',', index=False)
    elif(format == 'hyphy'):
        filename =  (os.path.join(filepath, '%s_nodes.ibf' % number))
        matrix_dict = matrix.to_dict()
        zipped = list(zip(matrix_dict['Node ID'].values(), matrix_dict['Source Node'].values(), matrix_dict['Internal Length'].values(), matrix_dict['Tip Length'].values()))
        to_write = '{'

        for x in zipped:
            to_write += '{ ' + ','.join([str(x).strip() for x in x]) + '}'

        to_write += '}'

        with open(filename, 'w') as f:
            f.write(to_write)

    else:
        raise Exception('invalid format you POS!')

def edge_creator(internal_length, tip_length, matrix_node_count, format):
    results = matrix_maker(internal_length,tip_length,matrix_node_count)
    matrix_writer(results, format)

def main():

    parser = argparse.ArgumentParser(description='Edge Maker')
    parser.add_argument('-c', '--count', help='Matrix node count', required=True, type=int)
    parser.add_argument('-f', '--format', help='Print to CSV or HyPhy format', default='csv', choices=['csv', 'hyphy'])

    args = parser.parse_args()

    internal_length = 0.005
    tip_length = 0

    matrix_node_count = args.count
    format = args.format
    edge_creator(internal_length, tip_length, matrix_node_count, format)


if __name__ == "__main__":
    main()
