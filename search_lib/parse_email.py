import re


def parse_email(filename, include_content=False):
    email_metadata = {}
    email_content = ""
    word_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as email_file:
            metadata_section = True
            for line in email_file:
                email_content += line

                if line == "\n":
                    metadata_section = False

                if metadata_section:
                    metadata = _parse_metadata_(line)
                    if metadata:
                        email_metadata[metadata[0]] = metadata[1]
                else:
                    line = line.strip()
                    split_strings = re.split('\W', line)
                    new_words = [word.lower() for word in split_strings if word]
                    word_list.extend(new_words)

        subject_words = re.split('\W', email_metadata['Subject'])
        word_list.extend([word.lower() for word in subject_words if word])

        if 'To' in email_metadata:
            word_list.append(email_metadata['To'])
        word_list.append(email_metadata['From'])
    except UnicodeDecodeError:
        pass

    content_value = email_content if include_content else None
    return email_metadata, word_list, content_value


def _parse_metadata_(line):
    try:
        [key, value] = line.split(":", 1)
    except ValueError:
        return None

    value = value.strip()

    if key == 'Message-ID':
        id_comps = value[1:-1].split(".")
        value = id_comps[0] + "." + id_comps[1]

    if key in ['Message-ID', 'Date', 'From', 'To', 'Subject']:
        return key, value
    else:
        return None


if __name__ == '__main__':
    print(parse_email("/home/aman/PycharmProjects/testa/maildir/allen-p/all_documents/1."))