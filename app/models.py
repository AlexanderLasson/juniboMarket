from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    file  = models.FileField(upload_to='uploads')
    total_sales_amount = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    preview_image = models.ImageField(upload_to='previews', null=True, blank=True)
    mockup_image = models.ImageField(upload_to='mockups', null=True, blank=True)
    current = models.BooleanField(default=True)
    status = models.CharField(default="pending")


    def __str__(self) -> str:
        return self.name

class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    return_policy = models.BinaryField(default=False)

    def __str__(self):
        return f"{self.customer_email}, {self.stripe_payment_intent}"
