from flask import Flask, request, render_template, jsonify
from rdkit import Chem
from rdkit.Chem import Draw
import base64
import io

app = Flask(__name__)

# Data collected from genrative ai 
solvents = {
    "Nucleophilic Substitution (SN2)": [
        {
            "name": "Dimethylformamide (DMF)", 
            "yield": "85-95%",
            "smiles": "CN(C)C=O"
        },
        {
            "name": "Acetonitrile", 
            "yield": "80-90%",
            "smiles": "CC#N"
        },
        {
            "name": "DMSO", 
            "yield": "75-85%",
            "smiles": "CS(=O)C"
        }
    ],
    "Grignard Reaction": [
        {
            "name": "Diethyl Ether", 
            "yield": "70-90%",
            "smiles": "CCOCC"
        },
        {
            "name": "THF", 
            "yield": "75-85%",
            "smiles": "C1CCOC1"
        }
    ],
    "Oxidation": [
        {
            "name": "Dichloromethane", 
            "yield": "80-90%",
            "smiles": "ClCCl"
        },
        {
            "name": "Acetone", 
            "yield": "70-80%",
            "smiles": "CC(=O)C"
        }
    ],
    "Reduction": [
        {
            "name": "THF", 
            "yield": "85-95%",
            "smiles": "C1CCOC1"
        },
        {
            "name": "Ethanol", 
            "yield": "70-80%",
            "smiles": "CCO"
        }
    ]
}

@app.route('/')
def index():
    reactions = list(solvents.keys())
    return render_template('index.html', reactions=reactions)

@app.route('/results', methods=['POST'])
def results():
    reaction = request.form['reaction']
    recommended_solvents = solvents.get(reaction, [])
    
    # Generate molecular structures for each solvent
    for solvent in recommended_solvents:
        try:
            mol = Chem.MolFromSmiles(solvent['smiles'])
            img = Draw.MolToImage(mol)
            
            # Convert image to base64 for HTML display
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            solvent['structure'] = base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            print(f"Error processing structure for {solvent['name']}: {str(e)}")
            solvent['structure'] = ''
    
    return render_template('results.html', 
                         reaction=reaction, 
                         solvents=recommended_solvents)

# RESTful API endpoints
@app.route('/api/reactions', methods=['GET'])
def get_reactions():
    """List all reactions"""
    return jsonify({
        'reactions': list(solvents.keys())
    })

@app.route('/api/reactions/<reaction>', methods=['GET'])
def get_reaction(reaction):
    """Get a specific reaction and its solvents"""
    if reaction not in solvents:
        return jsonify({'error': 'Reaction not found'}), 404
    return jsonify({
        'reaction': reaction,
        'solvents': solvents[reaction]
    })

@app.route('/api/reactions', methods=['POST'])
def create_reaction():
    """Create a new reaction"""
    data = request.get_json()
    reaction_name = data.get('reaction')
    reaction_solvents = data.get('solvents')
    
    if not reaction_name or not reaction_solvents:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if reaction_name in solvents:
        return jsonify({'error': 'Reaction already exists'}), 409
        
    solvents[reaction_name] = reaction_solvents
    return jsonify({
        'message': 'Reaction created',
        'reaction': reaction_name
    }), 201

@app.route('/api/reactions/<reaction>', methods=['PUT'])
def update_reaction(reaction):
    """Update a reaction's solvents"""
    if reaction not in solvents:
        return jsonify({'error': 'Reaction not found'}), 404
        
    data = request.get_json()
    new_solvents = data.get('solvents')
    
    if not new_solvents:
        return jsonify({'error': 'Missing solvents data'}), 400
        
    solvents[reaction] = new_solvents
    return jsonify({
        'message': 'Reaction updated',
        'reaction': reaction
    })

@app.route('/api/reactions/<reaction>', methods=['DELETE'])
def delete_reaction(reaction):
    """Delete a reaction"""
    if reaction not in solvents:
        return jsonify({'error': 'Reaction not found'}), 404
        
    del solvents[reaction]
    return jsonify({
        'message': 'Reaction deleted',
        'reaction': reaction
    })

if __name__ == '__main__':
    app.run(debug=True)



