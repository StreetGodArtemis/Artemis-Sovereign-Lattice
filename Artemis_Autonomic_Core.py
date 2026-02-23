# Artemis Autonomic Core: Heart-Lung Sync
# Author: Jerry Wayne Dawson Jr. | Nashville, TN

def sync_cardiopulmonary(brain_state, macro_body):
    """
    Syncs Heart (modes 96-120) and Lungs (modes 144-192)
    based on Brain Arousal parameters.
    """
    arousal = brain_state.arousal_value
    heart_bpm = 60.0 + (arousal * 40.0)
    breath_rate = 12.0 + (arousal * 8.0)
    
    macro_body.update_rates(heart_bpm, breath_rate)
    print(f"🫁 Autonomic Sync: {heart_bpm:.1f} BPM / {breath_rate:.1f} BR")
