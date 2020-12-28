from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import FileSystemStorage
import os,json
import pickle
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


#Loading model and tokenizer
model_test = load_model('finalized_model2.pkl')

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


#Classifying the prediction classes
def mapping_function(value):
        if value == 0:
            return 'Normal'
        elif value == 1:
            return 'Spam'
        else:
            return 'Error'  # eg. as undefined

def predict_spam(predict_msg):
    max_len = 50 
    trunc_type = "post" 
    padding_type = "post" 
    oov_tok = "<OOV>" 
    vocab_size = 500
    new_seq = tokenizer.texts_to_sequences(predict_msg)
    padded = pad_sequences(new_seq, maxlen =max_len,
                      padding = padding_type,
                      truncating=trunc_type)
    return((model_test.predict(padded) > 0.5).astype("int32"))



def predictJson(request):
        data = request.POST.get('sms')
        data = request.body.decode('latin-1')

        decode_data = json.loads(data)
        dataF = pd.DataFrame({'x':decode_data}).transpose()
        datalist = dataF['sms'].tolist()
        print(datalist)
        predict = predict_spam(datalist)

        mapped_vals = map(mapping_function,predict)
            # if you want a list
        classification = list(mapped_vals)
        #Change arraylist to string value
        classify = ', '.join(classification)
        sms_data = ', '.join(datalist)
      
        return JsonResponse({'classify':classify},safe=False)
        


def predictFile(request):
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name,fileObj)
    filePathName = fs.url(filePathName)
    filePath ='.'+filePathName
    data = pd.read_csv(filePath)
    data_lst = data.values.tolist()
    predict_fs = predict_spam(data_lst)

    ed_vals = map(mapping_function,predict_fs)
    # if you want a list
    mapped_list = list(ed_vals)
    
    sms_class = {j:k for j,k in zip(data['message'],mapped_list)}
    sms_class = sorted(sms_class.items(),key=lambda x: x[1],reverse=True)
    return JsonResponse({'sms_class':sms_class})

