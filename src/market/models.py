# -*- coding: utf-8 -*-

import csv
import sys
import uuid

from django.db import models

from desafio.settings import FILE_UPLOAD_PATH

# Constantes 
STATUS_UPLOADED = 'U'
STATUS_PROCESSED = 'P'
STATUS_MAP = {STATUS_UPLOADED: 'Importado', STATUS_PROCESSED: 'Processado'}

PURCHASER_NAME_ATTR = 'purchaser_name'
ITEM_DESCRIPTION_ATTR = 'item_description'
ITEM_PRICE_ATTR = 'item_price'
PURCHASE_COUNT_ATTR = 'purchase_count'
MERCHANT_ADDRESS_ATTR = 'merchant_address'
MERCHANT_NAME_ATTR = 'merchant_name'
CSF_FILE_ATTRIBUTES = [PURCHASER_NAME_ATTR, ITEM_DESCRIPTION_ATTR, ITEM_PRICE_ATTR, PURCHASE_COUNT_ATTR, MERCHANT_ADDRESS_ATTR, MERCHANT_NAME_ATTR]

# Classes
class BatchImport(models.Model):
    filename = models.CharField(max_length=255)
    file_location = models.CharField(max_length=1000)
    total_lines = models.IntegerField()
    imported_lines = models.IntegerField()
    purchase_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=1)
    created_date = models.DateTimeField(auto_now=True)
        
    @classmethod
    def create(cls, tempFile):
        bi = BatchImport()
        bi.filename = tempFile.name 
        bi.file_location = bi.upload_file(tempFile)
        bi.total_lines = -1
        bi.imported_lines = -1
        bi.purchase_amount = -1
        bi.status = STATUS_UPLOADED
        bi.save()
        
        return bi;
        
    def upload_file(self, temp_file):
        filename = "{}_{}".format(uuid.uuid4(), temp_file.name)
        full_filename = "{}/{}".format(FILE_UPLOAD_PATH, filename)
        with open(full_filename, 'wb+') as destination:
            for chunk in temp_file.chunks():
                destination.write(chunk)
    
        return filename
    
    def import_data(self):
        full_filename = "{}/{}".format(FILE_UPLOAD_PATH, self.file_location)
        with open(full_filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file,  fieldnames=CSF_FILE_ATTRIBUTES, dialect=csv.excel_tab)
            success_count = 0
            lines_count = 0
            for line in reader:
                if lines_count > 0:
                    if self.process_line(line):
                        success_count += 1
                lines_count += 1
            self.total_lines = lines_count - 1
            self.imported_lines = success_count
            self.status = STATUS_PROCESSED
            self.purchase_amount = self.calculate_amount()
            self.save();
    
    def calculate_amount(self):
        return sum([li.total for li in Order.objects.filter(batch_import=self)])
    
    def process_line(self, line):
        try:
            print "Iniciando processamento da linha: ", format(line)
            purchaser_name = self.get_str_attr_value(line, PURCHASER_NAME_ATTR)
            item_description = self.get_str_attr_value(line, ITEM_DESCRIPTION_ATTR)
            item_price = self.get_float_attr_value(line, ITEM_PRICE_ATTR)
            purchase_count = self.get_int_attr_value(line, PURCHASE_COUNT_ATTR)
            merchant_address = self.get_str_attr_value(line, MERCHANT_ADDRESS_ATTR)
            merchant_name = self.get_str_attr_value(line, MERCHANT_NAME_ATTR)
            
            purchaser = Customer.get_or_create(purchaser_name)
            item = Product.get_or_create(item_description)
            merchant = Seller.get_or_create(merchant_name, merchant_address)
            Order.create(purchaser, merchant, item, item_price, purchase_count, self)
        except:
            # Adicionar linha no arquivo de erro
            print "Erro ao processar linha:", sys.exc_info()[0]
            return False
        
        return True
    
    
    def get_str_attr_value(self, line, attr):
        return line[attr].strip(' ')

    def get_float_attr_value(self, line, attr):
        value = self.get_str_attr_value(line, attr)
        return float(value)

    def get_int_attr_value(self, line, attr):
        value = self.get_str_attr_value(line, attr)
        return int(value)
                        
    def status_name(self):
        return STATUS_MAP[self.status]

class Customer(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_or_create(cls, purchaser_name):
        customer_list = Customer.objects.filter(name=purchaser_name);
        if len(customer_list) == 0:
            customer = Customer()
            customer.name = purchaser_name
            customer.save()
        else:
            customer = customer_list[0]
        
        return customer
    
    def __unicode__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_or_create(cls, merchant_name, merchant_address):
        seller_list = Seller.objects.filter(name=merchant_name, address=merchant_address)
        if len(seller_list) == 0:
            seller = Seller()
            seller.name = merchant_name
            seller.address = merchant_address
            seller.save()
        else:
            seller = seller_list[0]
            
        return seller
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    description = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_or_create(cls, item_description):
        product_list = Product.objects.filter(description=item_description)
        if len(product_list) == 0:
            product = Product()
            product.description = item_description
            product.save()
        else:
            product = product_list[0]
            
        return product
    
    def __unicode__(self):
        return self.description

class Order(models.Model):
    customer = models.ForeignKey(Customer)
    seller = models.ForeignKey(Seller)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    unity_value = models.DecimalField(max_digits=8, decimal_places=2)
    created_date = models.DateTimeField(auto_now=True)
    batch_import = models.ForeignKey(BatchImport)
    
    @classmethod
    def create(cls, purchaser, merchant, item, item_price, purchase_count, batch_import):
        order = Order()
        order.customer = purchaser
        order.seller = merchant
        order.product = item
        order.unity_value = item_price
        order.quantity = purchase_count
        order.batch_import = batch_import
        order.save()
        
        return order
    
    @property
    def total(self):
        return self.quantity * self.unity_value
    
    def __unicode__(self):
        return self.product.description
        