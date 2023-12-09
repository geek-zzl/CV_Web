from flask import Flask, render_template, request, abort
import base64
import os

app = Flask(__name__)

IMAGE_FOLDER = 'static/images'
IMAGE_PER_PAGE = 50


@app.route('/page2')
def page2():
    name = request.args.get('name')
    file_handler = str(int(name.split('.')[0])) + '_'
    ori = False
    task_dict = {}
    for i in range(1, 12):
        task_folder = os.path.join(os.getcwd(), 'static', 'rodeo', f'task_{i}_visualization_result')
        file_list = os.listdir(task_folder)
        image_list = []
        for file in file_list:
            if ori is False and file.startswith(file_handler) and file.endswith('.jpg') and 'ori' in file:
                print(os.path.join(task_folder, file))
                task_dict["ori"] = os.path.join(task_folder, file)
                ori = True
            if file.startswith(file_handler) and file.endswith('.jpg') and 'ori' not in file:
                print(os.path.join(task_folder, file))
                image_list.append(os.path.join(task_folder, file))
        if len(image_list) > 0:
            task_dict[f'task_{i}'] = image_list

    images = []
    for key, value in task_dict.items():
        if key == "ori":
            with open(value, 'rb') as f:
                image_data = f.read()
                encoded = base64.b64encode(image_data).decode('utf-8')
                images.append({
                    "source": "ori",
                    'name': value.split('\\')[-1],
                    'data': f'data:image/png;base64,{encoded}'
                })
        else:
            for i in range(len(value)):
                # 查找value[i]中task_3_visualization字符串中的数字
                task_num = int(value[i].split('\\')[-2].split('_')[1])
                with open(value[i], 'rb') as f:
                    image_data = f.read()
                    encoded = base64.b64encode(image_data).decode('utf-8')
                images.append({
                    "source": f'task_{task_num}',
                    'name': value[i].split('\\')[-1],
                    'data': f'data:image/png;base64,{encoded}'
                })
    return render_template('page_two.html', img_data=images)


@app.route('/page3', methods=['GET', 'POST'])
def page3():
    label_list = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
                  'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
                  'motorbike', 'person', 'pattedplant', 'sheep', 'sofa', 'tnain', 'tv']
    if request.method == 'POST':
        # 判断信息是否完整
        if not request.form.get('label'):
            return 'Invalid Request'
        label = request.form.get('label')
        if label.lower() not in label_list:
            return 'Invalid Request Because of Invalid Label'
        label = label.lower()
        label_file_dict = {}
        for i in range(1, 12):
            label_files = []
            task_folder = os.path.join(os.getcwd(), 'static', 'rodeo', f'task_{i}_visualization_result')
            file_list = os.listdir(task_folder)
            for file in file_list:
                if label in file and 'ori' not in file:
                    label_files.append(os.path.join(task_folder, file))
            label_files.sort()
            # 太多了
            label_file_dict[f'task_{i}'] = label_files[0:12]
        image_data_dict = {}
        for key, value in label_file_dict.items():
            image = []
            for i in range(len(value)):
                with open(value[i], 'rb') as f:
                    image_data = f.read()
                    encoded = base64.b64encode(image_data).decode('utf-8')
                image.append({
                    'name': value[i].split('\\')[-1],
                    'data': f'data:image/png;base64,{encoded}'
                })
            image_data_dict[key] = image
        label = label.capitalize()
        return render_template('page_there.html', img_data=image_data_dict, label=label)


@app.route('/')
def page1():
    page = request.args.get('page', default=1, type=int)
    image_files = os.listdir(IMAGE_FOLDER)
    if not image_files:
        abort(404)
    start_index = (page - 1) * IMAGE_PER_PAGE
    end_index = start_index + IMAGE_PER_PAGE
    selected_files = image_files[start_index:end_index]

    images = []
    if not selected_files:
        abort(404)
    for filename in selected_files:
        with open(os.path.join(IMAGE_FOLDER, filename), 'rb') as f:
            image_data = f.read()
            encoded = base64.b64encode(image_data).decode('utf-8')
        images.append({
            'name': filename,
            'data': f'data:image/png;base64,{encoded}'
        })
    return render_template('page_one.html', images=images, page=page)


if __name__ == '__main__':
    app.run()
