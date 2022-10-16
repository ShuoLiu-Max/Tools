import sys
import os
import re


def search_name():
    if len(sys.argv) != 5:
        print('Usage: regular.py -S SearchFilePath RegularExperision OutfilePath')
        sys.exit()

    file_name = sys.argv[2]
    regular =  sys.argv[3]
    output_file = sys.argv[4]

    out_f = open(output_file,'w+')

    count = 0
    if os.path.isfile(file_name):
        print('Match : {}'.format(regular))
        print('Analysizing {}'.format(file_name))
        with open(file_name, 'r') as f:
            f_data = f.readlines()
            for f_d in f_data:
                if re.search(regular, f_d):
                    result = re.search('\[(.*?\..*?)\]',f_d).group(1).strip()
                    out_f.write(result + '\n')
                    count += 1
        print('{} matching messages were found'.format(count))
        if count != 0:
            print('Write to {} file successfully!'.format(output_file))
    else:
        print('ERROR: File {} is not existed!'.format(file_name))

    out_f.close()


def request_cost_time():
    if len(sys.argv) < 5:
        print('Usage: regular.py -C SearchFilePath requestList OutfilePath')
        sys.exit()

    file_name = sys.argv[2]
    command_names =  sys.argv[3:-1]
    output_file = sys.argv[-1]

    out_f = open(output_file,'w+')

    count = 0
    if os.path.isfile(file_name):
        print('Analysizing {}'.format(file_name))

        result = {}  # save {request: {message_id : [startTime, endTime]}}
        for command_name in command_names:
            temp = {}    # message_id: {message_id : request}
            print('Search : {}'.format(command_name))
            with open(file_name, 'r') as f:
                f_data = f.readlines()
                for f_d in f_data:
                    if re.search(command_name, f_d):
                        lineNum = re.search('(.+?)\[', f_d).group(1).strip()
                        timeS = re.search('\[(.*?\..*?)\]', f_d).group(1).strip()
                        messageId = re.search('message_id = (0x.+),', f_d).group(1)
                        if result.get(command_name, False) == False:
                            result[command_name] = {messageId: [lineNum, timeS]}
                            count += 1
                        else:
                            result[command_name][messageId] = [lineNum, timeS]
                            count += 1
                        temp[messageId] = command_name
                    elif re.search('message_id', f_d):
                        messageId = re.search('message_id = (0x.+),', f_d).group(1)
                        timeE = re.search('\[(.*?\..*?)\]', f_d).group(1).strip()
                        if temp.get(messageId, 0):
                            result[temp.get(messageId)][messageId].append(timeE)
                            all_len = result[temp.get(messageId)][messageId].__len__()

        for command_name in result:
            out_f.write(command_name + '\n')
            for massage_id in result[command_name]:
                if result[command_name][massage_id].__len__() == all_len:
                    cost_time = format(float(result[command_name][massage_id][-1]) - float(result[command_name][massage_id][-2]),'.6f')
                    out_f.write(result[command_name][massage_id][0] + ' massage_id: ' + massage_id + ' cost_time: ' + cost_time + '\n')
                else:
                    out_f.write(result[command_name][massage_id][0] + ' massage_id: ' + massage_id + ' No Response!\n')
        
        print('{} matching messages were found'.format(count))
        if count != 0:
            print('Write to {} file successfully!'.format(output_file))
    else:
        print('ERROR: File {} is not existed!'.format(file_name))

    out_f.close()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-S':
        search_name()
    elif len(sys.argv) > 1 and sys.argv[1] == '-C':
        request_cost_time()
    elif len(sys.argv) > 1 and sys.argv[1] == '--help':
        print('''
    -S    = Search for RegularExperision in SearchFilePath and 
            output 'time' in OutfilePath
    -C    = Calculate for the lifetime of a request in the requestList in 
            SearchFilePath and output 'cost_time' in OutfilePath
    ''')
    else:
        print('''Usage

    regular.py -S SearchFilePath RegularExperision OutfilePath
    regular.py -C SearchFilePath requestList OutfilePath

    Run 'regular.py --help' for more information.''')