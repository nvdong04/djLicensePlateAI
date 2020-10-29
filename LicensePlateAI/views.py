from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import numpy as np
from os import path
from django.http import JsonResponse
from django.core import serializers
import base64
from django.core.files.base import ContentFile
import json
import random
import os
import cv2
import pytesseract
from datetime import date
from datetime import datetime
import glob
from django.core.cache import cache
import pymysql
from django.contrib.auth import login, authenticate
from .forms import *


# Create your views here.

def RegisterView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                # user = form.cleaned_data.get('username')
                messages.success(request, "Đăng ký thành công")
                return redirect('Core:login')
            except ObjectDoesNotExist:
                pass
        else:
            messages.info(request, "Lỗi đăng ký, vui lòng thử lại")
    content = {
        'form': form
    }
    return render(request, 'LicensePlateAI/manager/register.html', content)


class LoginView(View):
    def get(self, request):
        return render(request, "LicensePlateAI/manager/login.html")

    def post(self, request):
        user = request.POST['user']
        password = request.POST['pass']
        user = authenticate(request, username=user, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Login success!")
            return redirect("Core:dashboard")
        else:
            messages.info(request, "Tài khoản or mật khẩu không đúng")
            return render(request, "LicensePlateAI/manager/login.html")


class DashboardView(View):
    def get(self, request):
        return HttpResponse("response")


conn = pymysql.connect(host='localhost', user='root', password='', db='nhandienkhuonmat2020')
a = conn.cursor()


class WelcomeClass(View):
    def get(self, request):
        return render(request, "public/index.html")

    def post(self, requert):
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        ngay = today.strftime("%Y-%m-%d") + " 12:00"
        if (hour <= 12):
            sql = "SELECT id_user, tenbien,thoigian_guixe, thoigian_nhanxe  FROM tbl_user where thoigian_guixe <=" + "'" + ngay + "'"
        else:
            sql = "SELECT id_user, tenbien, thoigian_guixe, thoigian_nhanxe FROM tbl_user where thoigian_guixe >" + "'" + ngay + "'"
        # Thực thi câu lệnh truy vấn (Execute Query).
        conn = pymysql.connect(host='localhost', user='root', password='', db='nhandienkhuonmat2020')
        a = conn.cursor()
        a.execute(sql)
        records = a.fetchall()
        return JsonResponse({"thongbao": "thanhcong", 'data': records})

    def ready(self):
        pass  # startup code here


class DetectCamera(View):
    def get(self, request):
        # conn = pymysql.connect(host='localhost', user='root', password='', db='dkxt')
        # a = conn.cursor()
        # sql = "SELECT * FROM tbl_sinhvien"
        # #Thực thi câu lệnh truy vấn (Execute Query).
        # a.execute(sql)
        # data = a.fetchall()
        # return HttpResponse(data)
        return render(request, "public/DetectCamera.html")


def postFriend(request):
    if request.is_ajax and request.method == "POST":
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%Y-%m-%d %H:%M:%S")

        # request_getdata = json.loads(request.POST.get('link_anh', None))
        # save_file(request_getdata)

        # return JsonResponse({"thongbao": "thanhcong", 'data' : request_getdata})
        #
        # return  HttpResponse(text)
        sql = "SELECT id_user, tenbien, thoigian_guixe, thoigian_nhanxe FROM tbl_user"
        # Thực thi câu lệnh truy vấn (Execute Query).
        a.execute(sql)
        records = a.fetchall()
        return JsonResponse({"thongbao": "thanhcong", 'data': records})

        id = ""
        # for row in request_getdata:
        #    id += random_id(15, "AWLCSLZOW120213", row['link_anh'])
        #    insert = "INSERT INTO `tbl_hinhanh` VALUES ("+id+",'" + row['link_anh']+ "',"+ str(count) +")"
        #     # a.execute(insert)
        #     # a.commit()
        # dulieu = JsonResponse({"data": request_getdata, 'thongbao' : 'thanhcong'})

    return JsonResponse({"thongbao": "thatbai", 'data': ''})


def random_id(length, string, alpha):
    id = ''
    for i in range(0, length, 2):
        id += random.choice(string)
        id += random.choice(alpha)
    return id


def save_file(request_getdata):
    for row in request_getdata:
        imgdata = base64.b64decode(str(row['link_anh']))
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%Y")
        path = 'static/public/img/' + dt_string + '_User_1'

        filename = path + "/" + str(row['id'] + 1) + '.jpg'
        if not os.path.exists(path):
            id_user = dt_string + '_User_1'
            insert = "INSERT INTO `tbl_user`(`id_user`,`biensoxe`) VALUES('" + str(id_user) + "','" + str(
                id_user) + "')"
            a.execute(insert)
            conn.commit()
            os.mkdir(path)
        else:
            newest = max(glob.iglob('static/public/img/' + now.strftime("%d_%m_%Y") + '_User_*'), key=os.path.getctime)

            if (newest.replace("\\", "/") == path and len(glob.glob(newest.replace("\\", "/") + "/*.jpg")) < 6):
                filename = path + "/" + str(row['id'] + 1) + '.jpg'
            else:
                if (len(glob.glob(newest.replace("\\", "/") + "/*.jpg")) >= 6):
                    i = str(int(newest.replace("\\", "/").split("_")[4]) + 1)
                    path = 'static/public/img/' + dt_string + '_User_' + i
                    os.mkdir(path)
                    filename = path + "/" + str(row['id'] + 1) + '.jpg'
                    id_user = newest.replace("\\", "/").split("/")[3]
                    insert = "INSERT INTO `tbl_user`(`id_user`,`biensoxe`) VALUES('" + str(id_user) + "','" + str(
                        id_user) + "')"
                    a.execute(insert)
                    conn.commit()
                else:
                    path = newest.replace("\\", "/")
                    filename = path + "/" + str(row['id'] + 1) + '.jpg'

        # if os.path.exists(filename):
        #     os.remove(filename)

        with open(filename, 'wb') as f:
            f.write(imgdata)
            text = detext(f.name)
            return HttpResponse(text)
            # id += random_id(15, "AWLCSLZOW120213", row['link_anh'])
            # insert = "INSERT INTO `tbl_hinhanh` VALUES ("+id+",'" + row['link_anh']+ "',"+ str(count) +")"
            # a.execute(insert)
            # a.commit()
            f.close()


def detext(anh):
    ## LOAD THU VIEN VA MODUL CAN THIET

    # ----------------------DOC HINH ANH - TACH HINH ANH NHAN DIEN--------------------
    img = cv2.imread(anh)
    # cv2.imshow('HINH ANH GOC', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, h = cv2.findContours(thresh, 1, 2)
    largest_rectangle = [0, 0]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x, y, w, h = cv2.boundingRect(largest_rectangle[1])

    image = img[y:y + h, x:x + w]
    cv2.drawContours(img, [largest_rectangle[1]], 0, (0, 255, 0), 8)

    cropped = img[y:y + h, x:x + w]
    # cv2.imshow('DANH DAU DOI TUONG', img)

    cv2.drawContours(img, [largest_rectangle[1]], 0, (255, 255, 255), 18)

    # --------------------- DOC HINH ANH CHUYEN THANH FILE TEXT-----------------------------
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # cv2.imshow('CROP', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    configr = (
        '-l eng --oem 1 --psm 6-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz0123456789')
    data = pytesseract.image_to_string(invert, lang='eng', config=configr)
    return data


class chonbienso(View):
    def get(self, request):
        return render(request, "public/chonbienso.html")


def nhandienHinhAnh(request):
    if request.is_ajax and request.method == "POST":
        request_getdata = json.loads(request.POST.get('link_anh', None))
        imgdata = base64.b64decode(request_getdata)
        path = 'media_root/image/'
        filename = path + '/HinhAnhNhanDien.jpg'
        if not os.path.exists(path):
            os.mkdir(path)
        with open(filename, 'wb') as f:
            f.write(imgdata)
            f.close()
        bienso = detext(filename)


        return JsonResponse({"thongbao": "thanhcong", 'data': bienso})



class NhanDienView(View):
    def get(self, request):
        return render(request, "public/chonbienso.html")

    def post(self, request):
        if request.is_ajax and request.method == "POST":
            link_img = json.loads(request.POST.get('link_anh', None))
            img_data = base64.b64decode(link_img)
            path = 'media_root/image/'
            filename = path + '/HinhAnhNhanDien.jpg'
            # if not os.path.exists(path):
            #     os.mkdir(path)
            # with open(filename, 'wb') as f:
            #     f.write(img_data)
            #     f.close()

            bienso = detext(filename).strip()
            vehicle_instance = vehicle.objects.create(vehicle_img=filename, vehicle_img_code=filename, vehicle_img_text=bienso)
            ticket_instance = ticket.objects.create(vehicle_id=vehicle.objects.last())
            return JsonResponse({"thongbao": "thanhcong", 'data': bienso})