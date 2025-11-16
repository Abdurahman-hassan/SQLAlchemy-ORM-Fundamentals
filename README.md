# SQLAlchemy ORM Fundamentals – File-by-File Guide

This project is a progressive walkthrough of SQLAlchemy ORM fundamentals using an e‑commerce‑style schema (Category, Product, User, Order, etc.).
Each numbered file introduces one or more new ORM concepts while keeping the domain model familiar.

---

## `001_declarative_mapping.py`
**Topic:** Declarative base class

- Defines a single `Base` class inheriting from `sqlalchemy.orm.DeclarativeBase`.
- This `Base` is the foundation for all ORM models in later files.
- No tables or columns yet – it only prepares the declarative mapping system.

---

## `002_defining_database_models.py`
**Topic:** Declaring models and `__tablename__`

- Reintroduces a `Base` class (same idea as in `001`).
- Defines empty ORM models with only `__tablename__`:
  - `Category`, `PromotionEvent`, `Product`, `ProductPromotionEvent`,
    `StockManagement`, `User`, `Order`, `OrderProduct`.
- Purpose is to demonstrate how to map Python classes to database tables using
  `__tablename__` before adding any columns or relationships.

---

## `003_common_field_types.py`
**Topic:** Common column types and basic constraints

- Adds typical SQLAlchemy column definitions on top of the models:
  - `String`, `Text`, `Boolean`, `SmallInteger`, `Integer`, `Numeric`.
- Examples:
  - `Category.name`, `Category.slug`, `Category.is_active`, `Category.level`.
  - `Product.name`, `Product.slug`, `Product.description`, `Product.is_digital`,
    `Product.is_active`, `Product.price` (with precision/scale `Numeric(10, 2)`).
  - `User.username`, `User.email`, `User.password`.
  - `StockManagement.quantity` and `OrderProduct.quantity`.
- Demonstrates:
  - How to attach column types to attributes.
  - Basic `nullable` and `unique` usage on user fields.

---

## `004_time_date_field.py`
**Topic:** Date, time and timestamp fields

- Extends the previous models with temporal types:
  - `Date` for `PromotionEvent.start_date` / `end_date`.
  - `DateTime` for audit fields like `created_at`, `updated_at` and
    `StockManagement.last_checked_at`.
- Uses `func.now()` for default timestamps and `onupdate=func.now()` for
  automatic update of `updated_at`.
- Demonstrates timezone‑aware `DateTime(timezone=True)` on `StockManagement`.

---

## `005_Required.py`
**Topic:** Required fields (`nullable=False`)

- Focuses on which columns must always have values:
  - Sets `nullable=False` on important business fields across models
    (e.g. names, slugs, description, timestamps, numeric values).
- Combines `nullable=False` with sensible defaults, e.g.:
  - `Category.is_active`, `Category.level`.
  - `Product.is_digital`, `Product.is_active`.
  - `StockManagement.quantity`.
- Shows how to make temporal and numeric fields required while still using
  defaults.

---

## `006_default_values.py`
**Topic:** Default values and required fields together

- Very similar to `005_Required.py`, reinforcing how to use defaults:
  - `default=` for booleans and integers (e.g. `is_active=False`, `level=0`,
    `quantity=0`).
  - `default=func.now()` for timestamps.
- Emphasizes the difference between `nullable=False` (required) and
  `default=` (what value is used when the app doesn’t set one explicitly).

---

## `007_unique_column.py`
**Topic:** Unique columns (`unique=True`)

- Adds `unique=True` on key identifying fields:
  - `Category.name`, `Category.slug`.
  - `PromotionEvent.name`.
  - `Product.name`, `Product.slug`.
  - `User.username`, `User.email`.
- Shows how unique constraints at the column level prevent duplicate values and
  help enforce business rules (e.g. no duplicate usernames).

---

## `008_primary_key.py`
**Topic:** Primary keys (`primary_key=True`) and autoincrement

- Introduces explicit integer primary keys for all tables:
  - `id = Column(Integer, primary_key=True, autoincrement=True)` on
    `Category`, `PromotionEvent`, `Product`, `ProductPromotionEvent`,
    `StockManagement`, `User`, `Order`, `OrderProduct`.
- Mentions (commented) example of **composite primary keys** via
  `PrimaryKeyConstraint`.
- Clarifies how primary keys uniquely identify rows and are the basis for
  relationships.

---

## `009_foreign_key.py`
**Topic:** One‑to‑many relationships and `ForeignKey`

- Adds foreign keys and simple relationships:
  - `Product.category_id = Column(ForeignKey("category.id"), nullable=False)`.
  - `Order.user_id = Column(ForeignKey("user.id"), nullable=False)`.
- Demonstrates bidirectional relationships using `relationship` and
  `back_populates`:
  - `Category.product` ↔ `Product.category` (a category has many products).
  - `User.orders` ↔ `Order.user` (a user has many orders).
- Contains extensive comments about hierarchical categories and how
  a self‑referencing foreign key could be used (though commented out here).

---

## `010_self_referencing_fk.py`
**Topic:** Self‑referencing foreign keys (hierarchical data)

- Implements a **self‑referencing foreign key** on `Category`:
  - `category_id = Column(ForeignKey("category.id", nullable=False))`.
- Shows how a record in `Category` can point to another category as its parent
  (tree/hierarchy structure).
- Keeps previous one‑to‑many relationships:
  - `Category.product` ↔ `Product.category`.
  - `User.orders` ↔ `Order.user`.
- Good reference for modeling category trees or nested structures.

---

## `011_on_delete.py`
**Topic:** `ondelete` behavior for foreign keys

- Adds `ondelete="RESTRICT"` to foreign keys to control delete behavior:
  - For self‑references on `Category.category_id`.
  - For `Product.category_id` and `Order.user_id`.
- `RESTRICT` prevents deleting a parent row when dependent rows still exist.
- Demonstrates how database‑level referential integrity rules protect your
  data when rows are deleted.

---

## `012_many_to_many.py`
**Topic:** Many‑to‑many relationships and association tables

- Introduces a classic many‑to‑many setup between `Product` and
  `PromotionEvent`:
  - Association table: `ProductPromotionEvent` with `product_id` and
    `promotion_event_id` foreign keys.
  - `PromotionEvent.products` and `Product.promotion_event` use
    `relationship(..., secondary="product_promotion_event", back_populates=...)`.
- Adds a `UniqueConstraint` on `(product_id, promotion_event_id)` in
  `ProductPromotionEvent` to prevent duplicate links.
- Keeps previous foreign key logic (e.g. `ondelete="RESTRICT"`).

---

## `013_one_to_one.py`
**Topic:** One‑to‑one relationships

- Models a **one‑to‑one** relationship between `Product` and `StockManagement`:
  - `StockManagement.product_id` is a `ForeignKey("product.id")` with
    `unique=True` to ensure one stock row per product.
  - `Product.stock = relationship("StockManagement", uselist=False, single_parent=True, back_populates="product")`.
- Reuses earlier many‑to‑many mapping between `Product` and `PromotionEvent`.
- Includes comments explaining why `unique=True` + `uselist=False` model a
  one‑to‑one constraint.

---

## `014_constraints.py`
**Topic:** Advanced `CheckConstraint` and business rules

- Concentrates many examples of `CheckConstraint` to enforce:
  1. **String rules** – not empty, trimmed, specific regex formats, SEO‑friendly slugs,
     username patterns, email format, etc.
  2. **Numeric rules** – positive price, discount range, non‑negative quantity,
     even numbers, minimum age, rating range.
  3. **Boolean logic** – allowed values for flags and compound conditions
     (e.g. featured product requires stock).
  4. **Date/time logic** – start date before end date, future events,
     `created_at <= updated_at`, max event duration, etc.
  5. **Business rules** – salary vs minimum wage, discount not exceeding price,
     stock requirements for active products, etc.
  6. **Enum‑like constraints** – enforcing allowed values for status/gender.
  7. **Cross‑field logic** – invariants across multiple columns (e.g.
     digital products must not have stock, admin must have a role).
- Also keeps the many‑to‑many `ProductPromotionEvent` with a composite
  unique constraint.
- Serves as a catalog of how far you can go with database‑level validation.

---

## `015_event_listener.py`
**Topic:** ORM event listeners (`@event.listens_for`)

- Shows how to use SQLAlchemy events to manipulate data in Python before it is
  written to the database:
  - Defines an event listener `lowercase_category_fields` for `Category`.
  - Hooks to both `before_insert` and `before_update`.
  - Automatically lowercases `Category.name` and `Category.slug`.
- Combines event listeners with constraints and relationships:
  - `Category` still participates in the `Product` relationship.
  - `Product` keeps many‑to‑many with `PromotionEvent` and one‑to‑one with
    `StockManagement`.
  - `Product` includes basic `CheckConstraint`s on `name`/`slug`.

---

## `016_trigger.py`
**Topic:** Database triggers + ORM event listeners

- Demonstrates how to use **database‑level triggers** together with
  SQLAlchemy’s Python‑side events.
- Defines a raw SQL DDL string (`trigger_sql`) that:
  - Creates a PostgreSQL function `lowercase_category_fields()`.
  - Creates a trigger `category_lowercase_trigger` on the `category` table to
    lowercase `name` and `slug` on every insert/update.
- Registers this DDL to run `after_create` of `Category.__table__`.
- Also defines the same Python‑side listener `lowercase_category_fields` used
  in `015_event_listener.py`, so both the ORM and the database enforce the
  same behavior.
- Keeps the rest of the schema consistent:
  - Many‑to‑many between `Product` and `PromotionEvent`.
  - One‑to‑one between `Product` and `StockManagement`.
  - Check constraints on `Product` for non‑empty and formatted `name`/`slug`.

---

## Supporting Files

### `pyproject.toml`
- Python project configuration (build system, dependencies, tool config, etc.).
- Likely used by tools like `poetry`, `pdm`, or `uv` to manage dependencies and
  packaging.

### `requirement.txt`
- Traditional pip requirements file.
- Lists Python dependencies (most importantly SQLAlchemy) to install with:
  `pip install -r requirement.txt`.

### `uv.lock`
- Lockfile generated by the `uv` packaging tool.
- Pins exact dependency versions for reproducible environments.

---

## How to Use This Guide

- Read the files in numeric order (`001` → `016`) together with this document.
- Each step introduces one or more SQLAlchemy ORM features on the same domain
  model so you can see how the schema evolves.
- Use it as a quick reference when you forget how to declare a relationship,
  add a constraint, or hook into events/triggers.

