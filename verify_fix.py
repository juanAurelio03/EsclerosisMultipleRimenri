
import sys
from pathlib import Path
import inspect

# Add project root to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

try:
    from src.ai import DualAIConsultation
    
    print("Successfully imported DualAIConsultation")
    
    consultor = DualAIConsultation()
    
    if hasattr(consultor, '_build_prompt'):
        print("✅ DualAIConsultation has attribute '_build_prompt'")
        
        # Check if it is a method
        if inspect.ismethod(consultor._build_prompt):
            print("✅ '_build_prompt' is a method")
        else:
            print("❌ '_build_prompt' is NOT a method")
            
    else:
        print("❌ DualAIConsultation does NOT have attribute '_build_prompt'")

except Exception as e:
    print(f"❌ Error during verification: {e}")
