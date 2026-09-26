import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shadenova.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder configuration for product images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()
    # Add sample products if table is empty
    if not Product.query.first():
        p1 = Product(title="Anti-Glare Glasses", price=499.0, description="Protect your eyes from digital screens.")
        p2 = Product(title="Travel Lens Case", price=199.0, description="Compact travel case for contact lenses.")
        db.session.add_all([p1, p2])
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# --- Naya Image Upload Route ---
@app.route('/admin/upload', methods=['GET', 'POST'])
def admin_upload():
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        description = request.form['description']
        
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Naya product database me save karna
            new_product = Product(title=title, price=price, description=description)
            db.session.add(new_product)
            db.session.commit()
            
        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)