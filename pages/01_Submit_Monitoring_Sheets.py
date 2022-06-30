import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
import os
from warnings import warn
import six
from PIL import Image
import datetime
import asposeomrcloud.apis.storage_api as storage_api
from asposeomrcloud.configuration import Configuration
from asposeomrcloud.apis.omr_api import OmrApi
from asposeomrcloud.models import OmrFunctionParam

from collections import OrderedDict
st.set_page_config(initial_sidebar_state="collapsed")

PATH_TO_OUTPUT = './temp'
TEMPLATE_NAME = 'Aspose_test'
TEMPLATE_DST_NAME = TEMPLATE_NAME + '.txt'
TEMPLATE_IMAGE_NAME = TEMPLATE_NAME + '.png'
TEMPLATE_USER_IMAGES_NAMES = ['photo.png']
LOGOS_FOLDER_NAME = 'Logos'
TEMPLATE_LOGOS_IMAGES_NAMES = ['logo1.jpg', 'logo2.png']


def serialize_files(file_paths):
    """
    Serialize files to JSON object
    :param file_paths: array of input file paths
    :return: JSON string with serialized files
    """
    d = OrderedDict([('Files', [])])
    for file_path in file_paths:
        try:
            with open(file_path, 'r+b') as f:
                data = f.read()

            encoded_data = str(base64.b64encode(data)) if six.PY2 else base64.b64encode(data).decode("ascii")

            d['Files'].append(OrderedDict([('Name', os.path.split(file_path)[1]), ('Size', os.path.getsize(file_path)),
                                           ('Data', encoded_data)]))
        except (IOError, OSError, EOFError) as err:
            text = "Can't read {} Reason: {} ".format(file_path, str(err))
            warn(text)
    return json.dumps(d, sort_keys=False, indent=4, separators=(', ', ': '))


def deserialize_file(file_info, dst_path):
    """
    Deserialize single response file to the specified location
    :param file_info: Response file to deserialize
    :param dst_path: Destination folder path
    :return: Path to deserialized file
    """
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    dst_file_path = os.path.join(dst_path, file_info.name)
    with open(dst_file_path, 'w+b') as f:
        f.write(base64.b64decode(file_info.data))
    print('File saved %s' % file_info.name)
    return dst_file_path


def deserialize_files(files, dst_path):
    """
    Deserialize list of files to the specified location
    :param files: List of response files
    :param dst_path: Destination folder path
    :return: Path to deserialized files
    """
    return [deserialize_file(file_info, dst_path) for file_info in files]


def upload_file(storage_api, src_file, dst_path):
    """
    Upload files to the storage
    :param src_file: Source file path
    :param dst_path: Destination path
    :return: None
    """

    # Upload file to storage
    print('Uploading %s into %s' % (src_file, dst_path))
    res = storage_api.upload_file(src_file, dst_path)
    print('Success!!! Uploaded file: ', res.uploaded)


def upload_demo_files(storage_api, data_dir_path):
    """
    Upload logo images used during template generation in a separate folder on cloud storage
    :data_dir_path: Path to directory containing logo images
    :return: None
    """

    response = storage_api.object_exists(path=str(LOGOS_FOLDER_NAME))
    if not response.exists:
        storage_api.create_folder(path=str(LOGOS_FOLDER_NAME))
    for logo in TEMPLATE_LOGOS_IMAGES_NAMES:
        dest_logo_path = '%s/%s' % (LOGOS_FOLDER_NAME, logo)
        response = storage_api.object_exists(path=str(dest_logo_path))
        if not response.exists:
            upload_file(storage_api, dest_logo_path, os.path.join(data_dir_path, logo))
        else:
            print('File %s already exists' % dest_logo_path)


def generate_template(omr_api, storage_api, template_dst_name, logos_folder):
    """
        Generate new template based on provided text description
        :param omr_api: OMR API Instance
        :param template_file_path: Path to template text description
        :param logos_folder: Name of the cloud folder with logo images
        :return: Generation response
    """

    image_file_name = os.path.basename(template_dst_name)

    # upload image on cloud
    upload_file(storage_api, image_file_name, template_dst_name)

    # provide function parameters
    omr_params = OmrFunctionParam(function_param=json.dumps(dict(ExtraStoragePath=logos_folder)), additional_param='')
    return omr_api.post_run_omr_task(image_file_name, "GenerateTemplate", omr_params)


def recognize_image(omr_api, storage_api, template_id, image_path):
    """
        Runs mark recognition on image
        :param omr_api: OMR API Instance
        :param template_id: Template ID
        :param image_path: Path to the image
        :return: Recognition response
    """

    image_file_name = os.path.basename(image_path)

    # upload image on cloud
    upload_file(storage_api, image_file_name, image_path)

    # provide template id as function parameter
    call_params = OmrFunctionParam(function_param=template_id, additional_param='')

    # call image recognition
    result = omr_api.post_run_omr_task(image_file_name, 'RecognizeImage', call_params)
    return result


def validate_template(omr_api, storage_api, template_image_path, template_data_dir):
    """
        Helper function that combines correct_template and finalize_template calls
        :param omr_api: OMR API Instance
        :param template_image_path: Path to template image
        :param template_data_dir: The folder where Template Data will be stored
        :return: Template ID
    """
    # Save correction results and provide them to the template finalization
    corrected_template_path = ''
    res_cr = correct_template(omr_api, storage_api, template_image_path, template_data_dir)
    if res_cr.error_code == 0:
        for file_info in res_cr.payload.result.response_files:
            response_file_local_path = deserialize_file(file_info, PATH_TO_OUTPUT)
            if file_info.name.lower().endswith('.omrcr'):
                corrected_template_path = response_file_local_path

    # Finalize template
    template_id = res_cr.payload.result.template_id
    res_fin = finalize_template(omr_api, storage_api, template_id, corrected_template_path)
    if res_fin.error_code == 0:
        deserialize_files(res_fin.payload.result.response_files, PATH_TO_OUTPUT)
    return template_id


def correct_template(omr_api, storage_api, template_image_path, template_data_dir):
    """
    Run template correction
    :param omr_api: OMR API Instance
    :param template_image_path: Path to template image
    :param template_data_dir: Path to template data file (.omr)
    :return: Correction response
    """

    image_file_name = os.path.basename(template_image_path)

    # upload template image
    upload_file(storage_api, image_file_name, template_image_path)

    # locate generated template file (.omr) and provide it's data as function parameter
    template_data_path = os.path.join(template_data_dir, os.path.splitext(image_file_name)[0] + '.omr')
    function_param = serialize_files([template_data_path])
    call_params = OmrFunctionParam(function_param=function_param, additional_param='')

    # call template correction
    result = omr_api.post_run_omr_task(image_file_name, "CorrectTemplate", call_params)
    return result


def finalize_template(omr_api, storage_api, template_id, corrected_template_path):
    """
    Run template finalization
    :param omr_api:  OMR API Instance
    :param template_id: Template id received after template correction
    :param corrected_template_path: Path to corrected template (.omrcr)
    :return: Finalization response
    """

    template_file_name = os.path.basename(corrected_template_path)

    # upload corrected template data on cloud
    upload_file(storage_api, template_file_name, corrected_template_path)

    # provide template id as function parameter
    call_params = OmrFunctionParam(function_param=template_id, additional_param='')

    # call template finalization
    result = omr_api.post_run_omr_task(template_file_name, 'FinalizeTemplate', call_params)
    return result

def run_analyzer(user_image):
    
    configuration = Configuration(apiKey=st.secrets["aspose_key"], appSid=st.secrets["aspose_client"])

    api = OmrApi(configuration)
    storage = storage_api.StorageApi(configuration)

    upload_demo_files(storage, './inputs')
    res_gen = generate_template(api, storage, os.path.join('./inputs', TEMPLATE_DST_NAME), LOGOS_FOLDER_NAME)
    if res_gen.error_code == 0:
        deserialize_files(res_gen.payload.result.response_files, PATH_TO_OUTPUT)
        
    # Step 2: Validate template
    template_id = validate_template(api, storage, './temp/Aspose_test.png', PATH_TO_OUTPUT)

    print("\t\tRecognize image...")
    res_rec = recognize_image(api, storage, template_id, os.path.join('./inputs', user_image))
    if res_rec.error_code == 0:
        result_file = deserialize_files(res_rec.payload.result.response_files, PATH_TO_OUTPUT)[0]

st.title("Magpasa ng papel pang obserba ng sintomas")
st.write('1. Piliin ang araw NA NAKASULAT SA PAPEL ng pasyente.')
date = st.date_input('Araw ng pag record')
st.write('2. Iclick ang allow sa pag gamit ng camera at picturan ang buong papel o mag upload ng larawan ng papel.')
st.write('3. Intayin ang kumpirmasyon na naupload ang resulta')
st.title("")
st.title("")
with st.form('Submission form'):
    image_main = st.camera_input(label='Kunan ng letrato ang papel', key='1')
   # image = c2.file_uploader('Mag upload ng larawan ng papel', type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Submit")
    if submitted:
        img = Image.open(image_main)
        st.image(image)
#        with st.spinner('Submission in progress'):
           # newImg1 = Image.open(image)
           # newImg1.save("./inputs/test.jpg")
           # run_analyzer('test.jpg')
           # sed = pd.read_csv('./temp/test.dat', header=None)
           # sed['key'] = sed[0].apply(lambda x: x.split(':')[0])
           # sed['value'] = sed[0].apply(lambda x: x.split(':')[1])
           # sed = sed.drop(columns=0)
           # sed = sed.T
           # new_header = sed.iloc[0]
           # sed = sed[1:]
           # sed.columns = new_header 
           # sed.insert(loc=0, column='Date', value=date)
           # sed.to_csv('patient_results.csv', mode='a', index=False, header=False)
     #   st.success('Salamat sa pag submit!')
        

footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p><a href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/">Return Home</a>
<p>Developed with ❤ by</p>
<p><strong>LinkX: Log and Information Exchange</strong></p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)
