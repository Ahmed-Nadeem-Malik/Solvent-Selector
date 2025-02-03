from flask import Flask, request, render_template
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

if __name__ == '__main__':
    app.run(debug=True)

