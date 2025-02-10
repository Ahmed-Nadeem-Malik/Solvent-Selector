from flask import Flask, request, render_template, redirect, url_for
from rdkit import Chem
from rdkit.Chem import Draw
import base64
import io
from models import db, Reaction, Solvent
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///solvents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    """Display the main page with all reactions."""
    reactions = Reaction.query.all()
    return render_template('index.html', reactions=reactions)

@app.route('/reaction/new', methods=['GET', 'POST'])
def new_reaction():
    """Create a new reaction."""
    if request.method == 'POST':
        name = request.form['name']
        if not Reaction.query.filter_by(name=name).first():
            reaction = Reaction(name=name)
            db.session.add(reaction)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('reaction_form.html')

@app.route('/reaction/<int:id>/edit', methods=['GET', 'POST'])
def edit_reaction(id):
    """Edit an existing reaction."""
    reaction = Reaction.query.get_or_404(id)
    if request.method == 'POST':
        reaction.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('reaction_form.html', reaction=reaction)

@app.route('/reaction/<int:id>/delete')
def delete_reaction(id):
    """Delete a reaction and its associated solvents."""
    reaction = Reaction.query.get_or_404(id)
    db.session.delete(reaction)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reaction/<int:id>/solvents')
def reaction_solvents(id):
    """Display solvents for a specific reaction."""
    reaction = Reaction.query.get_or_404(id)
    solvents = reaction.solvents
    
    # Generate molecular structures
    for solvent in solvents:
        try:
            mol = Chem.MolFromSmiles(solvent.smiles)
            img = Draw.MolToImage(mol)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            solvent.structure = base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            print(f"Error processing structure for {solvent.name}: {str(e)}")
            solvent.structure = ''
    
    return render_template('results.html', reaction=reaction, solvents=solvents)

@app.route('/solvent/new', methods=['GET', 'POST'])
def new_solvent():
    """Create a new solvent."""
    if request.method == 'POST':
        solvent = Solvent(
            name=request.form['name'],
            yield_range=request.form['yield_range'],
            smiles=request.form['smiles'],
            reaction_id=request.form['reaction_id']
        )
        db.session.add(solvent)
        db.session.commit()
        return redirect(url_for('reaction_solvents', id=request.form['reaction_id']))
    
    reactions = Reaction.query.all()
    return render_template('solvent_form.html', reactions=reactions)

@app.route('/solvent/<int:id>/edit', methods=['GET', 'POST'])
def edit_solvent(id):
    """Edit an existing solvent."""
    solvent = Solvent.query.get_or_404(id)
    if request.method == 'POST':
        solvent.name = request.form['name']
        solvent.yield_range = request.form['yield_range']
        solvent.smiles = request.form['smiles']
        solvent.reaction_id = request.form['reaction_id']
        db.session.commit()
        return redirect(url_for('reaction_solvents', id=solvent.reaction_id))
    
    reactions = Reaction.query.all()
    return render_template('solvent_form.html', solvent=solvent, reactions=reactions)

@app.route('/solvent/<int:id>/delete')
def delete_solvent(id):
    """Delete a solvent."""
    solvent = Solvent.query.get_or_404(id)
    reaction_id = solvent.reaction_id
    db.session.delete(solvent)
    db.session.commit()
    return redirect(url_for('reaction_solvents', id=reaction_id))

def init_db():
    """Initialize the database with sample data if it's empty."""
    if Reaction.query.first() is None:
        reactions_data = {
            "Nucleophilic Substitution (SN2)": [
                {
                    "name": "Dimethylformamide (DMF)", 
                    "yield_range": "85-95%",
                    "smiles": "CN(C)C=O"
                },
                {
                    "name": "Acetonitrile", 
                    "yield_range": "80-90%",
                    "smiles": "CC#N"
                },
                {
                    "name": "DMSO", 
                    "yield_range": "75-85%",
                    "smiles": "CS(=O)C"
                }
            ],
            "Grignard Reaction": [
                {
                    "name": "Diethyl Ether", 
                    "yield_range": "70-90%",
                    "smiles": "CCOCC"
                },
                {
                    "name": "THF", 
                    "yield_range": "75-85%",
                    "smiles": "C1CCOC1"
                }
            ],
            "Oxidation": [
                {
                    "name": "Dichloromethane", 
                    "yield_range": "80-90%",
                    "smiles": "ClCCl"
                },
                {
                    "name": "Acetone", 
                    "yield_range": "70-80%",
                    "smiles": "CC(=O)C"
                }
            ],
            "Reduction": [
                {
                    "name": "THF", 
                    "yield_range": "85-95%",
                    "smiles": "C1CCOC1"
                },
                {
                    "name": "Ethanol", 
                    "yield_range": "70-80%",
                    "smiles": "CCO"
                }
            ]
        }
        
        for reaction_name, reaction_solvents in reactions_data.items():
            reaction = Reaction(name=reaction_name)
            db.session.add(reaction)
            db.session.commit()
            
            for solvent_data in reaction_solvents:
                solvent = Solvent(
                    name=solvent_data['name'],
                    yield_range=solvent_data['yield_range'],
                    smiles=solvent_data['smiles'],
                    reaction_id=reaction.id
                )
                db.session.add(solvent)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_db()
    app.run(debug=True)



