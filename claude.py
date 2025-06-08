import modal
import anthropic
import os
import requests


claude_image = (
    modal.Image.debian_slim(python_version="3.10")
    # .apt_install("git")
    .pip_install("anthropic")
    .pip_install("requests")
    .env({"HALT_AND_CATCH_FIRE": "0"})
    # .run_commands("git clone https://github.com/modal-labs/agi && echo 'ready to go!'")
)


# # 1) Create a Modal App
app = modal.App("example-get-started")
# modal_key = "X5E-FRW-XCD"
ANTHROPIC_API_KEY = "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"


# Modal function to call Claude
@app.function(
    image=claude_image,
    secrets=[modal.Secret.from_name('anthropic-api-key')] # Attach the secret you created
)
def call_claude(model="claude-3-5-sonnet-20241022"):
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    data = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": f'Take the descriptions of challenges in two different papers and highlight similarities between them. The goal is to find common areas in disparate research fields that have the same goals or use the methodologies or concepts, but where this is not obvious. Output your analysis as a json file. The fields should be "cross_disciplinary_commonalities", "research_fields", and "meta_analysis". Within the cross_disciplinary_commonalities field, list your similarities as sub-fields named as the commonalities, with each commonality subdivided as “description” (state the link), "source" (theme in the first input), "target" (theme in the second input), “common_insight” (explain the link). Within "research_fields" state the "source_field" and "target_field" research fields. Within "meta_analysis", analyse in terms of "cross_disciplinary_potential”, "methodological_overlap”, "universal_principles”, “structural_analogies”, “Cross_cutting_themes”, and “shared_concepts”, where applicable.\n\nA central problem in motor control is understanding how the many biomechanical degrees of freedom are coordinated to achieve a common goal. An especially puzzling aspect of coordination is that behavioral goals are achieved reliably and repeatedly with movements rarely reproducible in their detail. Existing theoretical frameworks emphasize either goal achievement or the richness of motor variability, but fail to reconcile the two. Here we propose an alternative theory based on stochastic optimal feedback control. We show that the optimal strategy in the face of uncertainty is to allow variability in redundant (task-irrelevant) dimensions. This strategy does not enforce a desired trajectory, but uses feedback more intelligently, correcting only those deviations that interfere with task goals. From this framework, task-constrained variability, goal-directed corrections, motor synergies, controlled parameters, simplifying rules and discrete coordination modes emerge naturally. We present experimental results from a range of motor tasks to support this theory.\nControl of actions allows adaptive, goal-directed behaviour. The basal ganglia, including the subthalamic nucleus, are thought to play a central role in dynamically controlling actions through recurrent negative feedback loops with the cerebral cortex. Here, we summarize recent translational studies that used deep brain stimulation to record neural activity from and apply electrical stimulation to the subthalamic nucleus in people with Parkinson’s disease. These studies have elucidated spatial, spectral and temporal features of the neural mechanisms underlying the controlled delay of actions in cortico-subthalamic networks and demonstrated their causal effects on behaviour in distinct processing windows. While these mechanisms have been conceptualized as control signals for suppressing impulsive response tendencies in conflict tasks and as decision threshold adjustments in value-based and perceptual decisions, we propose a common framework linking decision-making, cognition and movement. Within this framework, subthalamic deep brain stimulation can lead to suboptimal choices by reducing the time that patients take for deliberation before committing to an action. However, clinical studies have consistently shown that the occurrence of impulse control disorders is reduced, not increased, after subthalamic deep brain stimulation surgery. This apparent contradiction can be reconciled when recognizing the multifaceted nature of impulsivity, its underlying mechanisms and modulation by treatment. While subthalamic deep brain stimulation renders patients susceptible to making decisions without proper forethought, this can be disentangled from effects related to dopamine comprising sensitivity to benefits versus costs, reward delay aversion and learning from outcomes. Alterations in these dopamine-mediated mechanisms are thought to underlie the development of impulse control disorders and can be relatively spared with reduced dopaminergic medication after subthalamic deep brain stimulation. Together, results from studies using deep brain stimulation as an experimental tool have improved our understanding of action control in the human brain and have important implications for treatment of patients with neurological disorders'}],
    }

    CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    
    print(response.json())
    
    try:
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            # Better error handling
            error_details = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            return f"Error {response.status_code}: {error_details}"
            
    except Exception as e:
        return f"Exception occurred: {str(e)}"




# modal token set --token-id ak-IbRoV8mnYAHBWsjfpeXQ0U --token-secret as-l2uFPba2Pn02UFiTcE2y6P 

# @app.function()
# def run_model():
    
#     ANTHROPIC_API_KEY = "X5E-FRW-XCD"
#     anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
#     # Claude API endpoint
#     CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

    
#     message = anthropic_client.messages.create(
#         model=os.getenv("CLAUDE_MODEL"),
#         max_tokens=1000,
#         temperature=0.3,
#         messages=[{"role": "user", "content": f'Take the descriptions of challenges in two different papers and highlight similarities between them. The goal is to find common areas in disparate research fields that have the same goals or use the methodologies or concepts, but where this is not obvious. Output your analysis as a json file. The fields should be "cross_disciplinary_commonalities", "research_fields", and "meta_analysis". Within the cross_disciplinary_commonalities field, list your similarities as sub-fields named as the commonalities, with each commonality subdivided as “description” (state the link), "source" (theme in the first input), "target" (theme in the second input), “common_insight” (explain the link). Within "research_fields" state the "source_field" and "target_field" research fields. Within "meta_analysis", analyse in terms of "cross_disciplinary_potential”, "methodological_overlap”, "universal_principles”, “structural_analogies”, “Cross_cutting_themes”, and “shared_concepts”, where applicable.\n\nA central problem in motor control is understanding how the many biomechanical degrees of freedom are coordinated to achieve a common goal. An especially puzzling aspect of coordination is that behavioral goals are achieved reliably and repeatedly with movements rarely reproducible in their detail. Existing theoretical frameworks emphasize either goal achievement or the richness of motor variability, but fail to reconcile the two. Here we propose an alternative theory based on stochastic optimal feedback control. We show that the optimal strategy in the face of uncertainty is to allow variability in redundant (task-irrelevant) dimensions. This strategy does not enforce a desired trajectory, but uses feedback more intelligently, correcting only those deviations that interfere with task goals. From this framework, task-constrained variability, goal-directed corrections, motor synergies, controlled parameters, simplifying rules and discrete coordination modes emerge naturally. We present experimental results from a range of motor tasks to support this theory.\nControl of actions allows adaptive, goal-directed behaviour. The basal ganglia, including the subthalamic nucleus, are thought to play a central role in dynamically controlling actions through recurrent negative feedback loops with the cerebral cortex. Here, we summarize recent translational studies that used deep brain stimulation to record neural activity from and apply electrical stimulation to the subthalamic nucleus in people with Parkinson’s disease. These studies have elucidated spatial, spectral and temporal features of the neural mechanisms underlying the controlled delay of actions in cortico-subthalamic networks and demonstrated their causal effects on behaviour in distinct processing windows. While these mechanisms have been conceptualized as control signals for suppressing impulsive response tendencies in conflict tasks and as decision threshold adjustments in value-based and perceptual decisions, we propose a common framework linking decision-making, cognition and movement. Within this framework, subthalamic deep brain stimulation can lead to suboptimal choices by reducing the time that patients take for deliberation before committing to an action. However, clinical studies have consistently shown that the occurrence of impulse control disorders is reduced, not increased, after subthalamic deep brain stimulation surgery. This apparent contradiction can be reconciled when recognizing the multifaceted nature of impulsivity, its underlying mechanisms and modulation by treatment. While subthalamic deep brain stimulation renders patients susceptible to making decisions without proper forethought, this can be disentangled from effects related to dopamine comprising sensitivity to benefits versus costs, reward delay aversion and learning from outcomes. Alterations in these dopamine-mediated mechanisms are thought to underlie the development of impulse control disorders and can be relatively spared with reduced dopaminergic medication after subthalamic deep brain stimulation. Together, results from studies using deep brain stimulation as an experimental tool have improved our understanding of action control in the human brain and have important implications for treatment of patients with neurological disorders'}],
#         )[0].text.strip()
#     print(message)
