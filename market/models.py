from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class ActivationLinks(models.Model):
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        related_name="+"
    )
    link = models.CharField(max_length=128)

    def __str__(self):
        return str(self.customer) + ":" + self.link


class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    reg_date = models.DateField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return ", ".join((self.name, self.email))


class Comment(models.Model):
    author = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    score = models.PositiveSmallIntegerField(
        choices=(
            (1, "★☆☆☆☆"),
            (2, "★★☆☆☆"),
            (3, "★★★☆☆"),
            (4, "★★★★☆"),
            (5, "★★★★★"),
        )
    )
    title = models.CharField(max_length=180)
    content = models.CharField(max_length=900)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return ", ".join((str(self.author), str(self.book)))

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("author", "book",)


class Book(models.Model):
    title = models.CharField(max_length=180)
    authors = models.ManyToManyField("Author", related_name="books")
    categories = models.ManyToManyField("Category", related_name="books")
    cover = models.ImageField(upload_to="covers")
    printed_year = models.PositiveSmallIntegerField()
    holders = models.ManyToManyField(
        "Customer",
        related_name="books",
        blank=True,
        editable=False
    )
    shoppers = models.ManyToManyField(
        "Customer",
        related_name="shopping_cart",
        blank=True,
        editable=False
    )
    score = models.DecimalField(
        max_digits=1,
        decimal_places=1,
        default=0,
        editable=False
    )

    def __str__(self):
        authors = ", ".join([str(author) for author in self.authors.all()])
        return ", ".join((
            self.title,
            authors,
            str(self.printed_year)
        ))
