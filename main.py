import csv
import re

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

FIO = '^(?P<lastname>[А-Яа-я]+)[\s+,](?P<firstname>[А-Яа-я]+)[\s+,]?(?P<surname>[А-Яа-я]+)?[\s+,]+$'
rfio = re.compile(FIO)

list_contacts = []

for idx, contact in enumerate(contacts_list):
  lastname = contact[0]
  firstname = contact[1]
  surname = contact[2]
  organization = contact[3]
  position = contact[4]
  phone = contact[5]
  email = contact[6]

  full_fio = lastname + ',' + firstname + ',' + surname + ','
  indices = [i for i, a in enumerate(full_fio) if a == ',']
  fio_match = [m.groupdict() for m in rfio.finditer(full_fio[:indices[2]])]
  if len(fio_match) > 0:

    if 'lastname' in fio_match[0]:
      lastname = fio_match[0]['lastname']
    if 'firstname' in fio_match[0]:
      firstname = fio_match[0]['firstname']
    if 'surname' in fio_match[0]:
      surname = fio_match[0]['surname']
    if phone in contact[5]:
      phone = re.sub(r"(\+7|8)\s?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*\(?(доб.)?\)?\s?(\d{4})\)?)?", r"+7(\2)\3-\4-\5 \7\8", str(phone))

    contact = [lastname, firstname, surname, organization, position, phone, email]
    if contact not in list_contacts:
      list_contacts.append(contact)
final_list = []
trash = []
trash_too = []
trash_set = set()
for contact in list_contacts:
  if contact[0] in trash_set:
    trash.append([x for x in list_contacts if x[0] == contact[0]])
    dublicate_list = [item for sublist in trash for item in sublist]

    dublicate_list[0][0] = dublicate_list[1][0]
    dublicate_list[0][1] = dublicate_list[1][1]
    dublicate_list[0][2] = dublicate_list[1][2]
    dublicate_list[0][6] = dublicate_list[1][6]

    final_list.append(dublicate_list[0])
    trash.clear()
    trash_too.append(contact[0])
  else:
    trash_set.add(contact[0])

list_contacts = [x for x in list_contacts if x[0] not in trash_too]

final_list = list_contacts + final_list

with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=",")
  datawriter.writerows(final_list)

