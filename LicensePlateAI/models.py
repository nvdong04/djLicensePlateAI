from django.db import models


TICKET_VEHICLE_TYPE_CHOICES = (
    ('CAR', 'Vé ô tô'),
    ('MOTOBIKE', 'Vé xe máy'),
    ('BIKE', 'Vé xe đạp')
)

TICKET_TYPE_CHOICES = (
    ('D', 'Vé ngày'),
    ('M', 'Vé tháng')
)

# Create your models here.
"""
tbl parking_lot: lưu trữ thông tin bãi  đỗ xe
number_of_blocks: số block có trong bãi đỗ xe
address : địa chỉ bãi đỗ xe
company_name: Tên công ty quản lý
"""


class parking_lot(models.Model):
    number_of_blocks = models.IntegerField()
    is_slot_available = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)


"""
table block - Lưu trữ thông tin các khối của bãi đẫu xe
parking_lot_id: block thuộc về khu đỗ xe nào
block_code: mã nhận dạng của block
number_of_floors: lưu trữ nố tầng nếu có
is_block_full: cho biết block này đã full chưa
"""


class block(models.Model):
    parking_lot_id = models.ForeignKey(parking_lot, on_delete=models.CASCADE)
    block_code = models.CharField(max_length=100)
    number_of_parking = models.IntegerField(default=1)
    is_block_full = models.BooleanField(default=False)


"""
table parking_slot: Lưu trũ thông tin về vị trí của bãi đỗ xe
block_id : vị trí thuộc khối để xe nào
slot_number: vị trí để xe số bao nhiêu
status: trạng thái của vị trí để xe
"""


class parking_slot(models.Model):
    block_id = models.ForeignKey(block, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    status = models.BooleanField(default=False)


"""
table ticket_type: lưu trữ các loại vé 
ticket_type_name: vé ngày, vé tháng ...
status: trạng thái
"""


class ticket_type(models.Model):
    ticket_type_name = models.CharField(choices=TICKET_TYPE_CHOICES, max_length=100)
    status = models.BooleanField(default=False)


"""
table ticket_vehicle_type: lưu trữ các xe và giá tiền 
ticket_vehicle_name: vé xe máy, vé ô tô....
price: giá tiền
"""


class ticket_vehicle_type(models.Model):
    ticket_vehicle_name = models.CharField(choices=TICKET_VEHICLE_TYPE_CHOICES, max_length=100)
    price = models.FloatField()


class vehicle(models.Model):
    vehicle_img = models.ImageField(upload_to='vehicle/%Y/%m/%d')
    vehicle_img_code = models.ImageField(upload_to='vehicle_code/%Y/%m/%d')
    vehicle_img_text = models.CharField(default='', max_length=255)

    def __str__(self):
        return self.vehicle_img_text


"""
table ticket : Lưu trữ thông tin vé xe
time_in: giờ vào
time_out: giờ ra
vehicle_id: 
"""


class ticket(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True, null=True)
    vehicle_id = models.ForeignKey(vehicle, on_delete=models.CASCADE)
    ticket_vehicle_type_id = models.ForeignKey(ticket_vehicle_type, on_delete=models.CASCADE)
    ticket_type_id = models.ForeignKey(ticket_type, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)



