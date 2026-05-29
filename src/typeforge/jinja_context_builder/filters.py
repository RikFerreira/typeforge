def pluck_first(list_records: list = None, key: str = None):
    if key is None:
        return f"{key} is not a valid key. Please provide a valid key to pluck_first filter."

    if list_records is None or len(list_records) == 0:
        return f"No records found. Please provide a valid list of records to pluck_first filter."

    first_record = list_records[0]

    if not isinstance(first_record, dict):
        return f"The first record is not a dictionary. Please provide a valid list of records to pluck_first filter."

    if key not in first_record:
        return f"Key << {key} >> not found in the first record. Please provide a valid key to pluck_first filter."

    return first_record[key]

# def multiple_check_boxes(value, domain):
#     print_dict = {a: '☑' if b else '☐' for a, b in zip(domain, [x == value for x in domain])}

#     string_buff = io.StringIO()

#     for key, value in print_dict.items():
#         string_buff.write(f'{value}\t{key}\n')

#     return string_buff.getvalue()

# def x_for_match(value, compare):
#     return "X" if value == compare else ""

# def export_picture_from_base_64(base64string, filename, output_dir = None):
#     if output_dir is None:
#         output_dir = self.temp_dir

#     output_file = os.path.join(output_dir, filename)

#     with open(output_file, 'wb') as fout:
#         fout.write(base64.decodebytes(base64string))

#     return output_file

# def render_picture_from_path(path, width = None, height = None):
#     # TODO: This method does not work well with portrait images. The method rotates the image before render.

#     section = self.input_template.get_docx().sections[0]
#     section_width = (section.page_width - (section.left_margin + section.right_margin)) * 1.0 / 36000

#     if width <= 1:
#         image_width = Mm(section_width) * width
#     else:
#         image_width = Mm(width)

#     if height:
#         image_height = Mm(height)
#     else:
#         image_height = height

#     return InlineImage(self.input_template, path, width = image_width, height = image_height)

# def pluck_highest(list_records):
#     return max(list_records) if list_records else None

# def pluck_lowest(list_records):
#     return min(list_records) if list_records else None