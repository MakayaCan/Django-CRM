from django.db import models
from django.core.exceptions import ValidationError
import re

# Validator for Zimbabwe phone numbers
def validate_zimbabwe_phone(value):
    pattern = r'^\+263\d{7,9}$'  # +263 followed by 7–9 digits
    if not re.match(pattern, value):
        raise ValidationError("Phone number must start with +263 and follow Zimbabwean number format.")

# List of AFM Provinces (32) for dropdown
AFM_PROVINCES = [
    ("Bulawayo West", "Bulawayo West"),
    ("Bulawayo North", "Bulawayo North"),
    ("Bulawayo South", "Bulawayo South"),
    ("Harare West", "Harare West"),
    ("Harare East", "Harare East"),
    ("Harare North", "Harare North"),
    ("Harare South", "Harare South"),
    ("Harare Central", "Harare Central"),
    ("Mvurwi", "Mvurwi"),
    ("Ruwa", "Ruwa"),
    ("Chitungwiza West", "Chitungwiza West"),
    ("Chitungwiza East", "Chitungwiza East"),
    ("Manicaland East", "Manicaland East"),
    ("Manicaland South", "Manicaland South"),
    ("Manicaland North", "Manicaland North"),
    ("Manicaland Central", "Manicaland Central"),
    ("Midlands South", "Midlands South"),
    ("Midlands Central", "Midlands Central"),
    ("Midlands North", "Midlands North"),
    ("Midlands East", "Midlands East"),
    ("Chinhoyi", "Chinhoyi"),
    ("Mashonaland East", "Mashonaland East"),
    ("Mashonaland Central", "Mashonaland Central"),
    ("Mashonaland North", "Mashonaland North"),
    ("Mashonaland West", "Mashonaland West"),
    ("Masvingo", "Masvingo"),
    ("Lowveld", "Lowveld"),
    ("Matebeleland North", "Matebeleland North"),
    ("Matebeleland East", "Matebeleland East"),
    ("Matebeleland South", "Matebeleland South"),
    ("Chivhu", "Chivhu"),
    ("Gokwe", "Gokwe"),
]

# Mapping keywords in city/district to AFM provinces (suggestions)
AFM_PROVINCE_MAP = {
    "harare": "Harare Central",
    "borrowdale": "Harare North",
    "glen view": "Harare South",
    "mabvuku": "Harare East",
    "avondale": "Harare West",
    "bulawayo": "Bulawayo South",   # default
    "nkulumane": "Bulawayo South",
    "luveve": "Bulawayo North",
    "magwegwe": "Bulawayo West",
    "chitungwiza": "Chitungwiza East",
    "zengeza": "Chitungwiza East",
    "st marys": "Chitungwiza West",
    "gweru": "Midlands Central",
    "mkoba": "Midlands South",
    "kwekwe": "Midlands North",
    "shurugwi": "Midlands East",
    "gokwe": "Gokwe",
    "masvingo": "Masvingo",
    "triangle": "Lowveld",
    "chivhu": "Chivhu",
    "bindura": "Mashonaland Central",
    "marondera": "Mashonaland East",
    "chinhoyi": "Chinhoyi",
    "kariba": "Mashonaland West",
    "mhangura": "Mashonaland North",
    "mutare": "Manicaland East",
    "chimanimani": "Manicaland South",
    "nyanga": "Manicaland North",
    "rusape": "Manicaland Central",
    "plumtree": "Matebeleland South",
    "lupane": "Matebeleland North",
    "binga": "Matebeleland East",
}

class Record(models.Model):
    # Auto-generated
    creation_date = models.DateTimeField(auto_now_add=True)

    # Individual details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10, 
        choices=[("Male", "Male"), ("Female", "Female")]
    )
    national_id = models.CharField(max_length=15, unique=True)
    marital_status = models.CharField(
        max_length=15, 
        choices=[
            ("Single", "Single"),
            ("Married", "Married"),
            ("Divorced", "Divorced"),
            ("Widowed", "Widowed")
        ]
    )
    fullname_spouse = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    dob = models.DateField()

    # Contact details
    phone_main = models.CharField(max_length=15, validators=[validate_zimbabwe_phone])
    phone_optional = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[validate_zimbabwe_phone]
    )
    address = models.CharField(max_length=255)

    # **New fields**
    
    province = models.CharField(max_length=50, choices=AFM_PROVINCES, default="Harare East")

    def save(self, *args, **kwargs):
        """
        Custom save method to:
        1. Auto-set fullname_spouse to 'N/A' if marital status is 'Single'.
        2. Auto-suggest province based on address if not set manually.
        """

        # ✅ Automatically set spouse name to "N/A" when single
        if self.marital_status == "Single":
            self.fullname_spouse = "N/A"
        else:
            # If not single, clear spouse name if not provided
            if not self.fullname_spouse:
                self.fullname_spouse = None

        # ✅ Auto-suggest province based on address or city_town_district
        if not self.province or self.province == "Harare East":  # default
            search_key = (getattr(self, "city_town_district", None) or self.address).lower()
            for key, province_name in AFM_PROVINCE_MAP.items():
                if key in search_key:
                    self.province = province_name
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

