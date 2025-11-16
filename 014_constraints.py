from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(ForeignKey("category.id", nullable=False, ondelete="RESTRICT"))

    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(55), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=False)
    level = Column(SmallInteger, nullable=False, default=0)

    product = relationship("Product", back_populates="category")


class PromotionEvent(Base):
    __tablename__ = "promotion_event"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price_reduction = Column(Integer, nullable=False)

    products = relationship(
        "Product",
        secondary="product_promotion_event",
        back_populates="promotion_event",
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(ForeignKey("category.id"), nullable=False, ondelete="RESTRICT")

    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(55), nullable=False, unique=True)
    description = Column(Text, nullable=False)  # No length limit
    is_digital = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # 10 digits, 2 decimal places

    category = relationship("Category", back_populates="product")

    promotion_event = relationship(
        "PromotionEvent",
        secondary="product_promotion_event",
        back_populates="products",
    )

    stock = relationship(
        "StockManagement",
        uselist=False,
        back_populates="product",
        single_parent=True,
    )

    __table_args__ = (
        ####################################################################
        # 🟩 1. STRING VALIDATION (التحقق من صحة النصوص)
        ####################################################################

        # ✅ الاسم لا يمكن أن يكون نصاً فارغاً
        CheckConstraint("name <> ''", name="chk_name_not_empty"),

        # ✅ الاسم لا يمكن أن يكون مسافات فقط (يتم عمل trim)
        CheckConstraint("trim(name) <> ''", name="chk_name_not_whitespace"),

        # ✅ الـ slug لا يمكن أن يكون فارغاً
        CheckConstraint("slug <> ''", name="chk_slug_not_empty"),

        # ✅ أحرف صغيرة فقط (بدون أرقام أو رموز)
        CheckConstraint("slug ~ '^[a-z]+$'", name="chk_lowercase_only"),

        # ✅ أحرف + أرقام فقط (بدون رموز)
        CheckConstraint("slug ~ '^[A-Za-z0-9]+$'", name="chk_alphanumeric"),

        # ✅ username يسمح بالأحرف والأرقام والـ underscore فقط
        CheckConstraint("username ~ '^[A-Za-z0-9_]+$'", name="chk_username"),

        # ✅ Slug pattern احترافي مناسب للـ SEO
        # (لا يسمح ببدء أو نهاية بـ hyphen ولا يسمح بـ double hyphen)
        CheckConstraint(
            "slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'",
            name="chk_slug_format_seo"
        ),

        # ✅ الاسم يحتوي على أحرف ومسافات فقط
        CheckConstraint("name ~ '^[A-Za-z ]+$'", name="chk_letters_spaces"),

        # ✅ صيغة الإيميل (متوسطة التعقيد)
        CheckConstraint(
            "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="chk_email_format"
        ),

        ####################################################################
        # 🟦 2. NUMERIC RULES (التحقق من الأرقام)
        ####################################################################

        # ✅ السعر يجب أن يكون ≥ 0
        CheckConstraint("price >= 0", name="chk_price_positive"),

        # ✅ الخصم يجب أن يكون بين 0 و 100
        CheckConstraint("discount BETWEEN 0 AND 100", name="chk_discount_range"),

        # ✅ الكمية لا يمكن أن تكون سالبة
        CheckConstraint("quantity >= 0", name="chk_quantity_valid"),

        # ✅ الرقم يجب أن يكون زوجي
        CheckConstraint("value % 2 = 0", name="chk_even_number"),

        # ✅ الحد الأدنى للعمر (مثلاً ≥ 18)
        CheckConstraint("age >= 18", name="chk_age_min_18"),

        # ✅ تقييم من 1 إلى 5
        CheckConstraint("rating >= 1 AND rating <= 5", name="chk_rating_1_5"),

        ####################################################################
        # 🟧 3. BOOLEAN LOGIC (التحقق من المنطق الشرطي)
        ####################################################################

        # ✅ is_active يجب أن يكون 0 أو 1 فقط
        CheckConstraint("is_active IN (0, 1)", name="chk_is_active_bool"),

        # ✅ المنتج لا يمكن أن يكون مميزاً مع stock = 0
        CheckConstraint(
            "NOT(is_featured AND quantity = 0)",
            name="chk_featured_requires_stock"
        ),

        ####################################################################
        # 🟨 4. DATE & TIME (التحقق من التواريخ)
        ####################################################################

        # ✅ تاريخ البداية يجب أن يكون قبل النهاية
        CheckConstraint("start_date < end_date", name="chk_event_dates"),

        # ✅ تاريخ الحدث يجب أن يكون في المستقبل
        CheckConstraint("event_date > now()", name="chk_future_event"),

        # ✅ created_at ≤ updated_at
        CheckConstraint("created_at <= updated_at", name="chk_timestamp_order"),

        ####################################################################
        # 🟥 5. BUSINESS LOGIC RULES (قواعد العمل)
        ####################################################################

        # ✅ الراتب ≥ الحد الأدنى
        CheckConstraint("salary >= minimum_wage", name="chk_salary_min"),

        # ✅ لا يمكن تفعيل المنتج بدون stock
        CheckConstraint(
            "NOT(is_active AND quantity = 0)",
            name="chk_active_needs_stock_full"
        ),

        # ✅ الخصم لا يمكن أن يكون أكبر من السعر
        CheckConstraint("discount <= price", name="chk_discount_le_price"),

        # ✅ مدة الفعالية يجب ألا تتعدى 30 يومًا
        CheckConstraint(
            "(end_date - start_date) <= interval '30 days'",
            name="chk_event_duration"
        ),

        ####################################################################
        # 🟪 6. ENUM-LIKE RULES (اختيارات ثابتة)
        ####################################################################

        # ✅ status يجب أن يكون من القيم المحددة
        CheckConstraint(
            "status IN ('pending', 'paid', 'canceled')",
            name="chk_status_enum"
        ),

        # ✅ gender قيمة ثابتة
        CheckConstraint(
            "gender IN ('male', 'female')",
            name="chk_gender_enum"
        ),

        ####################################################################
        # 🟫 7. CROSS-FIELD LOGIC (التحقق بين حقلين)
        ####################################################################

        # ✅ المنتج الرقمي لا يجب أن يكون لديه stock
        CheckConstraint(
            "NOT(is_digital AND quantity > 0)",
            name="chk_digital_no_stock"
        ),

        # ✅ المستخدم إذا كان admin يجب أن يكون له role
        CheckConstraint(
            "NOT(is_admin AND role IS NULL)",
            name="chk_admin_role_required"
        ),

        # ✅ الفعالية ذات التخفيض صفر يجب أن تكون غير مفعلة
        CheckConstraint(
            "NOT(price_reduction = 0 AND is_active = true)",
            name="chk_zero_reduction_inactive"
        ),
    )


class ProductPromotionEvent(Base):
    __tablename__ = "product_promotion_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False
    )
    promotion_event_id = Column(
        Integer, ForeignKey("promotion_event.id", ondelete="RESTRICT"), nullable=False
    )

    __table_args__ = (
        # Ensures that the combination of product_id and promotion_event_id is unique
        # this is need for the many-to-many relationship
        UniqueConstraint(
            "product_id", "promotion_event_id", name="unique_product_event"
        ),
    )


class StockManagement(Base):
    __tablename__ = "stock_management"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        ForeignKey("product.id", ondelete="RESTRICT"), nullable=False, unique=True
    )

    quantity = Column(Integer, nullable=False, default=0)
    last_checked_at = Column(DateTime(timezone=True), nullable=False)

    product = relationship("Product", back_populates="stock")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("user.id", nullable=False, ondelete="RESTRICT"))

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="orders")


class OrderProduct(Base):
    __tablename__ = "order_product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
