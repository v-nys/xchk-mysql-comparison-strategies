from xchk_core.strats import CheckingPredicate, Strategy, OutcomeComponent, OutcomeAnalysis, StratInstructions

# TODO: aanpassen
MYSQL_PW = 'in-het-echt-geheim'
unspecified_db_cmd = ['mysql', '-u', 'root', '-h', 'mysql', f'--password={MYSQL_PW}']
model_db_cmd = ['mysql', '-u', 'root', '-h', 'mysql', f'--password={MYSQL_PW}', 'ModernWaysBL']
student_db_cmd = ['mysql', '-u', 'root', '-h', 'mysql', f'--password={MYSQL_PW}', 'ModernWays']

# algemene strategie
# 1) calibratie -> kan dit doen door Strategy te subclassen
# 2) uitvoeren eigenlijke scripts (model en student) en controle op output beide scripts (te testen + aan te passen aan access control)
# 3) controle op tabelstructuur
# 4) controle op aanwezige data
# ???) controle op gelijke constraints, was er nog niet

class ExecutedScriptHasMatchingOutputCheck(CheckingPredicate):

    def __init__(self,model_path):
        super().__init__()
        self.model_path = model_path

    def instructions(self,exercise_name):
        """Returns a hierarchical representation of the explicit conditions to be met for this check to return `True`."""
        return [f"{exercise_name}.sql produceert dezelfde uitvoer als de modeloplossing"]

    def negative_instructions(self,exercise_name):
        """Returns a hierarchical representation of the explicit conditions to be met for this check to return `False`."""
        return [f"{exercise_name}.sql produceert een andere uitvoer dan de modeloplossing"]

    def component_checks(self):
        return []

    def check_submission(self,submission,student_path,desired_outcome,init_check_number,ancestor_has_alternatives,parent_is_negation=False,open=open):
        entry = f'{submission.exercise.slug}.sql'
        with open(model_path) as fh:
            model_script_result = subprocess.run(unspecified_db_cmd,text=True,input=fh.read(), capture_output=True)
        with open(os.path.join(student_path,entry)) as fh:
            student_script_result = subprocess.run(unspecified_db_cmd,text=True,input=fh.read(), capture_output=True)
        same_outputs = model_script.stdout == student_script.stdout and model_script.stderr == student_script.stderr
        if desired_outcome and not same_outputs:
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=False,
                                         desired_outcome=desired_outcome,
                                         # TODO: kan misschien diff gebruiken?
                                         rendered_data=f'<p>Jouw script produceert een andere output dan de modeloplossing. Jouw script produceert op de output stream:<br>{student_script_result.stdout}<br>Jouw script produceert op de error stream:<br>{student_script_result.stderr}</p><p>Het modelscript produceert op de output stream:<br>{model_script_result.stdout}<br>He tmodelscript produceert op de error stream:<br>{model_script_result.stderr}</p>',
                                         acceptable_to_ancestor=ancestor_has_alternatives)
        elif not desired_outcome and same_outputs:
            # willen verschillende output maar is niet zo
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=True,
                                         desired_outcome=desired_outcome,
                                         rendered_data=f'<p>De output stream en error stream van jouw script produceren identiek identiek hetzelfde als de output stream en error stream van de modeloplossing.</p>',
                                         acceptable_to_ancestor=ancestor_has_alternatives)
        else:
            component = OutcomeComponent(component_number=init_check_number,
                                         outcome=same_outputs,
                                         desired_outcome=desired_outcome, # = same_outputs
                                         rendered_data=None,
                                         acceptable_to_ancestor=True)
        return OutcomeAnalysis(outcome=same_outputs,
                               outcomes_components=[component])

# if desired, define strategies by subclassing Strategy
# override __init__ so that refusing_check and accepting_check are hardwired
