# 📚 How to Populate Languages in Production

Your application has a management command that will add all languages and their course levels to the database.

## Languages Included:

1. **Japanese** 🇯🇵
2. **Chinese** 🇨🇳
3. **Hebrew** 🇮🇱
4. **Korean** 🇰🇷
5. **Russian** 🇷🇺
6. **Dutch** 🇳🇱
7. **Swedish** 🇸🇪
8. **Arabic** 🇸🇦
9. **French** 🇫🇷
10. **Spanish** 🇪🇸
11. **Italian** 🇮🇹
12. **German** 🇩🇪

## How to Run in Production (Render):

### Step 1: Access Render Shell

1. Go to **Render Dashboard** → Your `ifla-backend` service
2. Click **"Shell"** tab (top navigation)
3. This opens a terminal where you can run Django commands

### Step 2: Run the Command

Type this command:

```bash
python manage.py populate_languages
```

### Step 3: Verify

The command will:
- ✅ Create all 12 languages if they don't exist
- ✅ Create course levels (A1, A2, B1, B2, C1, C2) for each language
- ✅ Skip languages that already exist (won't duplicate)

### Expected Output:

```
Created language: Japanese
  Created level: A1
  Created level: A2
  Created level: B1
  Created level: B2
  Created level: C1
  Created level: C2
Created language: Chinese
  ...
Successfully populated language and course data!
```

---

## Running Locally (for testing):

If you want to test locally first:

```bash
python manage.py populate_languages
```

---

## Course Levels Created for Each Language:

Each language gets 6 levels:
- **A1** - Beginner
- **A2** - Elementary  
- **B1** - Intermediate
- **B2** - Upper Intermediate
- **C1** - Advanced
- **C2** - Proficient

---

## Pricing (Category 1 - Asian Languages):

- A1: ₹16,000
- A2: ₹18,000
- B1: ₹20,000
- B2: ₹22,000
- C1: ₹24,000
- C2: ₹26,000

**Languages**: Japanese, Chinese, Hebrew, Korean, Russian, Dutch, Swedish

---

## Pricing (Category 2 - European Languages):

- A1: ₹14,000
- A2: ₹16,000
- B1: ₹18,000
- B2: ₹20,000
- C1: ₹22,000
- C2: ₹24,000

**Languages**: Arabic, French, Spanish, Italian, German

---

## After Running the Command:

1. Languages will appear on `/languages` page
2. Users can enroll in any language
3. Course levels will be available for selection
4. Pricing will be correct for each level

---

## If Languages Already Exist:

The command uses `get_or_create`, so:
- ✅ It won't create duplicates
- ✅ It will only add missing languages
- ✅ Existing languages are safe

You can run it multiple times safely!

---

## Need to Add More Languages?

Edit `courses/management/commands/populate_languages.py` and add new language entries, then run the command again.

