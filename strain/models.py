from django.db import models


class Strain(models.Model):
    strain_name = models.CharField(db_column="Strain", primary_key=True, max_length=20)

    @property
    def lt_sixty_days_count(self):
        return self.mice.filter()

    @property
    def sixty_to_one_eighty_days_count(self):
        return self.mice.filter()

    @property
    def one_eighty_days_to_one_year_count(self):
        return self.mice.filter()

    @property
    def one_to_two_year_count(self):
        return self.mice.filter()
    
    @property
    def 

    def __str__(self):
        return f"{self.strain_name}"

    class Meta:
        managed = True
        db_table = "strain"
