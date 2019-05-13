import pandas as pd
import scipy.stats
import argparse
import os

dirname = os.path.dirname(os.path.realpath(__file__))
rv = scipy.stats.beta(2.6711811991141117, 0.9048171772138711, -0.00148892720428367, 0.016488927204283674)

def matrix_maker_dist(matrix_node_count):
    #print('\n         generating the matrix... \n' )
    nodes = list(range(int(matrix_node_count)))
    ## payload for column 1 (node ID) ##
    j = [i +1 for i in nodes]
    #print('Total number of  nodes in the network: ' + str(j[-1]) + '\n')

    ## payload for column 2 (source nodes) ##
    nodes[0] = -1

    ## payload for columns 3 ( internal length) and 4 (tip length) ##
    temp_internal = [rv.rvs() for i in nodes]
    temp_tip = [0.0 for i in nodes]
    #print(len(j), len(nodes), len(temp_internal), len(temp_tip))
    d = {'Node ID': j, 'Source Node': nodes, 'Internal Length': temp_internal, 'Tip Length':temp_tip}
    df = pd.DataFrame(d)
    return df

def matrix_maker(internal, tip, matrix_node_count):
    #print('\n         generating the matrix... \n' )
    nodes = list(range(int(matrix_node_count)))
    ## payload for column 1 (node ID) ##
    j = [i +1 for i in nodes]
    #print('Total number of  nodes in the network: ' + str(j[-1]) + '\n')

    ## payload for column 2 (source nodes) ##
    nodes[0] = -1

    ## payload for columns 3 ( internal length) and 4 (tip length) ##
    temp_internal = [internal for i in nodes]
    temp_tip = [tip for i in nodes]
    #print(len(j), len(nodes), len(temp_internal), len(temp_tip))
    d = {'Node ID': j, 'Source Node': nodes, 'Internal Length': temp_internal, 'Tip Length':temp_tip}
    df = pd.DataFrame(d)
    return df


def matrix_writer(matrix, format, output_fn):
    #print('\n         writing the matrix to a file... \n' )
    node_number = str(len(matrix))
    #index_number = str(matrix_node_index)
    #print('\n          this is inside matrix writer... \n')
    #print(node_number,index_number)

    #filepath =  (os.path.join(dirname, 'data/matrix/'))

    if(format == 'csv'):
        print('sorry charlie')
        ## this will get buggy need to specify .csv ##
        #filename =  (os.path.join(filepath, output_fn))
        #print(filename)
        #matrix.to_csv(filename, sep=',', index=False)
    elif(format == 'hyphy'):
        #filename =  (os.path.join(filepath, output_fn))
        filename = output_fn
        #print(filename)
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

def edge_creator_dist(matrix_node_count, format, output_fn):
    results = matrix_maker_dist(matrix_node_count)
    matrix_writer(results, format, output_fn)
    return results


def edge_creator(internal_length, tip_length, matrix_node_count, format, output_fn):
    results = matrix_maker(internal_length,tip_length,matrix_node_count)
    matrix_writer(results, format, output_fn)
    return results

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
