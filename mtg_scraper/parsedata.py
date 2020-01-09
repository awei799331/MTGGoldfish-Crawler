def parse_helper():
    lines = []
    with open('temp_file.txt', 'r') as textf:
        content = textf.readlines()
        content = [x.strip() for x in content]
        counter = 0
        all_found = False
        while counter < len(content):
            print("d += \"\\n" in content[counter])
            if "d += \"\\n" in content[counter]:
                lines.append(content[counter].replace("d += \"\\n", "").replace("\";", ""))
                all_found = True
            elif all_found:
                break
            counter+=1

        del content
        textf.close()

    print(lines)
    with open("output.csv", "w") as output:
        for x in lines:
            output.write(x + '\n')
        output.close()

parse_helper()