import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, Product

# Flask app initialization
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shadenova.db'
app.config['SECRET_KEY'] = 'samnova_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Database with App
db.init_app(app)

with app.app_context():
    db.create_all()

# Home Route - Show all products
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Product Detail Route - Show single product info
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Admin Route - Add new product
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        description = request.form['description']
        
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Save product to database
            new_product = Product(title=title, price=price, description=description, image_file=filename)
            db.session.add(new_product)
            db.session.commit()
            
        return redirect(url_for('home'))
        
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)