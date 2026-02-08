from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Todo
from app.forms import RegistrationForm, LoginForm, TodoForm

def register_routes(app):
    """Register all routes with the app"""
    
    # ==================== HOME ====================
    @app.route('/')
    def index():
        """Home page - redirect based on auth status"""
        if current_user.is_authenticated:
            return redirect(url_for('todos'))
        return redirect(url_for('login'))
    
    # ==================== AUTHENTICATION ====================
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration"""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('todos'))
        
        form = RegistrationForm()
        
        if form.validate_on_submit():
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data.lower()
            )
            user.set_password(form.password.data)
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        # Redirect if already logged in
        if current_user.is_authenticated:
            return redirect(url_for('todos'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            # Find user by email
            user = User.query.filter_by(email=form.email.data.lower()).first()
            
            # Check password
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'👋 Welcome back, {user.username}!', 'success')
                
                # Redirect to next page or todos
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('todos'))
            else:
                flash('❌ Invalid email or password!', 'danger')
        
        return render_template('login.html', form=form)
    
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        flash('👋 You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    
    
    @app.route('/todos')
    @login_required
    def todos():
        """View all todos for current user"""
        
        status_filter = request.args.get('status', 'all')
        
     
        if status_filter == 'all':
            user_todos = Todo.query.filter_by(user_id=current_user.id)\
                         .order_by(Todo.created_at.desc()).all()
        else:
            user_todos = Todo.query.filter_by(user_id=current_user.id, status=status_filter)\
                         .order_by(Todo.created_at.desc()).all()
        
      
        stats = {
            'total': Todo.query.filter_by(user_id=current_user.id).count(),
            'incomplete': Todo.query.filter_by(user_id=current_user.id, status='incomplete').count(),
            'in_progress': Todo.query.filter_by(user_id=current_user.id, status='in_progress').count(),
            'complete': Todo.query.filter_by(user_id=current_user.id, status='complete').count()
        }
        
        return render_template('todos.html', todos=user_todos, stats=stats, current_filter=status_filter)
    
    
    @app.route('/todo/add', methods=['GET', 'POST'])
    @login_required
    def add_todo():
        """Add new todo"""
        form = TodoForm()
        
        if form.validate_on_submit():
            todo = Todo(
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                user_id=current_user.id
            )
            
            db.session.add(todo)
            db.session.commit()
            
            flash('✅ Todo added successfully!', 'success')
            return redirect(url_for('todos'))
        
        return render_template('todo_form.html', form=form, title='Add New Todo')
    
    
    @app.route('/todo/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_todo(id):
        """Edit existing todo"""
        todo = Todo.query.get_or_404(id)
        
        
        if todo.user_id != current_user.id:
            flash('Access denied!', 'danger')
            return redirect(url_for('todos'))
        
        form = TodoForm(obj=todo)
        
        if form.validate_on_submit():
            todo.title = form.title.data
            todo.description = form.description.data
            todo.status = form.status.data
            
            db.session.commit()
            
            flash('Todo updated successfully!', 'success')
            return redirect(url_for('todos'))
        
        return render_template('todo_form.html', form=form, title='Edit Todo')
    
    
    @app.route('/todo/delete/<int:id>')
    @login_required
    def delete_todo(id):
        """Delete todo"""
        todo = Todo.query.get_or_404(id)
        
        # Security check
        if todo.user_id != current_user.id:
            flash('Access denied!', 'danger')
            return redirect(url_for('todos'))
        
        db.session.delete(todo)
        db.session.commit()
        
        flash('Todo deleted successfully!', 'success')
        return redirect(url_for('todos'))
    
    
    @app.route('/todo/status/<int:id>/<status>')
    @login_required
    def update_status(id, status):
        """Quick status update"""
        todo = Todo.query.get_or_404(id)
        
        # Security check
        if todo.user_id != current_user.id:
            flash('Access denied!', 'danger')
            return redirect(url_for('todos'))
        
        # Validate status
        valid_statuses = ['incomplete', 'in_progress', 'complete']
        if status in valid_statuses:
            todo.status = status
            db.session.commit()
            flash(f'Status updated to {status.replace("_", " ").title()}!', 'success')
        else:
            flash(' Invalid status!', 'danger')
        
        return redirect(url_for('todos'))