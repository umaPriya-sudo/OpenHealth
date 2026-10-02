# ===== ENHANCED CHATBOT =====
def get_health_response(user_message):
    msg = user_message.lower().strip()

    if any(keyword in msg for keyword in [
        'diabetes',
        'diabetic',
        'blood sugar',
        'blood glucose',
        'high blood sugar',
        'high glucose',
        'sugar level',
        'sugar levels',
        'glucose level',
        'glucose levels',
        'insulin',
        'type 1 diabetes',
        'type 2 diabetes',
        'diabetes symptoms',
        'signs of diabetes',
        'diabetic symptoms'
    ]):

        return """📋 **DIABETES - Complete Information**

**🔴 What is Diabetes?**
Diabetes is a chronic condition where your body either doesn't produce enough insulin or can't effectively use the insulin it produces. This leads to high blood sugar levels.

**⚠️ Common Symptoms:**
• Increased thirst and frequent urination
• Extreme hunger
• Unexplained weight loss
• Fatigue and weakness
• Blurred vision
• Slow-healing sores or cuts
• Frequent infections
• Numbness in hands/feet

**🏥 Risk Factors:**
• Family history
• Obesity/overweight
• Sedentary lifestyle
• Age (45+)
• High blood pressure

**✅ Prevention Tips:**
• Maintain healthy weight (BMI 18.5-24.9)
• Exercise 30 minutes daily
• Eat balanced diet with whole grains
• Reduce sugar and refined carbs
• Regular health screenings

⚠️ **Consult a doctor for proper diagnosis and treatment!**"""

    if any(keyword in msg for keyword in [
        'heart',
        'heart disease',
        'heart problem',
        'heart problems',
        'heart attack',
        'cardiovascular',
        'cardiovascular disease',
        'cardiac',
        'cardiac disease',
        'heart symptoms',
        'heart health',
        'chest pain',
        'chest discomfort',
        'heart failure',
        'arrhythmia',
        'irregular heartbeat'
    ]):
        return """❤️ **HEART DISEASE - Complete Information**

**🔴 What is Heart Disease?**
Heart disease refers to several conditions affecting the heart, including coronary artery disease, heart attacks, arrhythmias, and heart failure.

**⚠️ Warning Signs:**
• Chest pain/discomfort (angina)
• Shortness of breath
• Pain in arms, back, neck, jaw
• Cold sweats
• Nausea/indigestion
• Dizziness/lightheadedness
• Extreme fatigue
• Swelling in legs/ankles

**🏥 Risk Factors:**
• High blood pressure
• High cholesterol
• Smoking
• Diabetes
• Obesity/overweight
• Sedentary lifestyle
• Family history

**✅ Prevention Tips:**
• Monitor blood pressure (target < 120/80)
• Lower cholesterol (LDL < 100)
• Exercise 150 min/week
• Eat heart-healthy diet (DASH/Mediterranean)
• Quit smoking
• Limit alcohol
• Manage stress
• Regular check-ups

⚠️ **Call emergency services immediately for chest pain!**"""

    if any(keyword in msg for keyword in [
        'breast cancer',
        'breast cancers',
        'breast lump',
        'breast lumps',
        'lump in breast',
        'breast tumor',
        'breast tumour',
        'mammogram',
        'breast symptoms',
        'breast changes',
        'breast swelling',
        'nipple discharge',
        'nipple changes',
        'breast pain'
    ]):
        return """🎀 **BREAST CANCER - Complete Information**

**🔴 What is Breast Cancer?**
Breast cancer is a disease where cells in the breast grow uncontrollably.

**⚠️ Warning Signs:**
• New lump in breast or armpit
• Thickening or swelling of breast
• Skin changes (dimpling, redness, scaling)
• Nipple changes (inversion, discharge)
• Breast pain
• Change in breast size/shape

**🏥 Risk Factors:**
• Female gender
• Age (50+)
• Family history/genetics (BRCA1/BRCA2)
• Dense breast tissue
• Hormone therapy
• Alcohol consumption
• Obesity

**✅ Prevention & Early Detection:**
• Monthly self-exams
• Regular mammograms (starting 40)
• Clinical breast exams
• Genetic testing if high risk
• Healthy lifestyle
• Maintain healthy weight
• Limit alcohol

⚠️ **Early detection saves lives! Consult a doctor regularly.**"""

        # ===== BRAIN TUMOR =====
    if any(keyword in msg for keyword in [
        'brain tumor',
        'brain tumour',
        'brain cancer',
        'brain tumor symptoms',
        'brain tumour symptoms',
        'brain tumor signs',
        'brain tumour signs',
        'brain swelling',
        'tumor in brain',
        'tumour in brain'
    ]):
        return """🧠 **BRAIN TUMOR - Complete Information**

**🔴 What is a Brain Tumor?**
A brain tumor is an abnormal growth of cells in or around the brain. Brain tumors can be benign or malignant.

**⚠️ Possible Symptoms:**
• Persistent or worsening headaches
• Nausea or vomiting
• Seizures
• Changes in vision
• Difficulty with balance or coordination
• Weakness or numbness
• Problems with speech or understanding
• Changes in memory or behavior

**🏥 Important:**
Symptoms can have many different causes and do not necessarily mean a person has a brain tumor.

**🩺 Diagnosis:**
Doctors may use neurological examinations and imaging tests such as MRI or CT scans to investigate symptoms.

⚠️ **If you experience new, severe, or worsening neurological symptoms, consult a healthcare professional promptly.**"""

        # ===== PARKINSON'S DISEASE =====
    if any(keyword in msg for keyword in [
        "parkinson's",
        "parkinson",
        "parkinsons",
        "parkinson disease",
        "parkinson's disease",
        "parkinson symptoms",
        "parkinson's symptoms",
        "parkinson signs",
        "parkinson's signs",
        "tremor",
        "hand tremor",
        "muscle stiffness",
        "slow movement"
    ]):
        return """⚡ **PARKINSON'S DISEASE - Complete Information**

**🔴 What is Parkinson's Disease?**
Parkinson's disease is a progressive disorder of the nervous system that can affect movement. Common motor symptoms include tremor, muscle stiffness, slowed movement, and balance problems. :chatgpt-content-reference{index="0"}

**⚠️ Common Symptoms:**
• Tremor or shaking, often beginning in a hand
• Muscle stiffness or rigidity
• Slowness of movement
• Balance or walking problems
• Changes in speech
• Difficulty with everyday movements

**🩺 Important:**
These symptoms can also occur in other conditions, so having one or more of them does not by itself establish Parkinson's disease. A healthcare professional should evaluate persistent or concerning symptoms. :chatgpt-content-reference{index="1"}

⚠️ **If you are concerned about Parkinson's symptoms, consult a qualified healthcare professional for proper evaluation.**"""


        # ===== MALARIA =====
    if any(keyword in msg for keyword in [
        'malaria',
        'malaria symptoms',
        'malaria signs',
        'signs of malaria',
        'symptoms of malaria',
        'malaria fever',
        'malaria infection',
        'malaria disease',
        'malaria test',
        'malaria diagnosis'
    ]):
        return """🦟 **MALARIA - Complete Information**

**🔴 What is Malaria?**
Malaria is an infectious disease caused by parasites and transmitted mainly through the bite of infected mosquitoes.

**⚠️ Common Symptoms:**
• Fever
• Chills
• Headache
• Muscle aches
• Tiredness or weakness
• Nausea or vomiting
• Diarrhea

**🩺 Diagnosis:**
Symptoms alone cannot confirm malaria. A healthcare professional should arrange appropriate laboratory testing, usually using a blood sample.

**🚨 Important:**
Malaria can become severe if diagnosis and treatment are delayed. If you have symptoms that could be malaria, seek medical attention promptly.

⚠️ **This information is not a diagnosis. Consult a healthcare professional for proper testing and treatment.**"""


    if any(keyword in msg for keyword in [
        'liver',
        'liver disease',
        'liver problem',
        'liver problems',
        'liver health',
        'hepatitis',
        'hepatitis a',
        'hepatitis b',
        'hepatitis c',
        'jaundice',
        'yellow skin',
        'yellow eyes',
        'liver symptoms',
        'liver damage',
        'fatty liver'
    ]):
        return """🧪 **LIVER DISEASE - Complete Information**

**⚠️ Common Symptoms:**
• Jaundice (yellow skin/eyes)
• Dark urine
• Pale stools
• Abdominal swelling
• Chronic fatigue
• Nausea/vomiting
• Loss of appetite
• Easy bruising
• Itchy skin

**🏥 Risk Factors:**
• Heavy alcohol use
• Obesity
• Diabetes
• Hepatitis B/C infection
• Family history

**✅ Prevention Tips:**
• Limit alcohol
• Get vaccinated (Hepatitis A/B)
• Safe sexual practices
• Don't share needles
• Maintain healthy weight
• Eat healthy diet
• Exercise regularly

⚠️ **Early detection is key! See a doctor if you have symptoms.**"""

    if any(keyword in msg for keyword in [
        'kidney',
        'kidney disease',
        'kidney problem',
        'kidney problems',
        'kidney health',
        'renal',
        'renal disease',
        'renal problem',
        'kidney symptoms',
        'kidney failure',
        'kidney damage',
        'kidney infection',
        'foamy urine',
        'swollen feet',
        'swelling in legs'
    ]):
        return """🫘 **KIDNEY DISEASE - Complete Information**

**⚠️ Common Symptoms:**
• Fatigue/weakness
• Changes in urination
• Swelling (edema)
• Shortness of breath
• Nausea/vomiting
• Loss of appetite
• Muscle cramps
• Foamy urine
• Dark urine

**🏥 Risk Factors:**
• Diabetes
• High blood pressure
• Heart disease
• Family history
• Age (60+)
• Obesity
• Smoking

**✅ Prevention Tips:**
• Control blood pressure
• Manage diabetes
• Stay hydrated
• Eat low-sodium diet
• Avoid NSAIDs
• Regular kidney function tests

⚠️ **Early detection is crucial! Get regular check-ups.**"""


        # ===== FEATURE SUGGESTION: SYMPTOM CHECKER =====
    if any(phrase in msg for phrase in [
        'i have',
        'i am having',
        "i'm having",
        'i am experiencing',
        "i'm experiencing",
        'i feel',
        "i'm feeling",
        'my symptoms',
        'my symptom',
        'suffering from',
        'experiencing'
    ]) and any(symptom in msg for symptom in [
        'fever',
        'headache',
        'cough',
        'cold',
        'pain',
        'stomach pain',
        'chest pain',
        'body pain',
        'fatigue',
        'weakness',
        'dizzy',
        'dizziness',
        'nausea',
        'vomiting',
        'breathing problem',
        'shortness of breath',
        'swelling',
        'rash',
        'sore throat',
        'diarrhea',
        'constipation'
    ]):
        return """🩺 **Symptom Checker**

It sounds like you're experiencing some symptoms.

You can use the **OpenHealth Symptom Checker** to explore your symptoms, possible causes, and precautions.

[ACTION:SYMPTOM_CHECKER]"""


        # ===== FEATURE SUGGESTION: FIND A DOCTOR =====
    if any(phrase in msg for phrase in [
        'i need a doctor',
        'i want a doctor',
        'find a doctor',
        'find doctor',
        'need a doctor',
        'looking for a doctor',
        'looking for doctor',
        'consult a doctor',
        'consult doctor',
        'see a doctor',
        'talk to a doctor',
        'speak to a doctor',
        'doctor consultation',
        'doctor appointment'
    ]):
        return """👨‍⚕️ **Find a Doctor**

You can find available doctors on OpenHealth and explore their specialization and consultation details.

[ACTION:FIND_DOCTOR]"""


        # ===== FEATURE SUGGESTION: MEDICINE RECOGNITION =====
    if any(phrase in msg for phrase in [
        'identify medicine',
        'identify a medicine',
        'identify this medicine',
        'recognize medicine',
        'recognize a medicine',
        'recognize this medicine',
        'what medicine is this',
        'which medicine is this',
        'medicine identification',
        'medicine recognition',
        'check this medicine',
        'check a medicine',
        'what is this medicine'
    ]):
        return """💊 **Medicine Recognition**

You can use OpenHealth's **Medicine Recognition** feature to identify a medicine from an image.

[ACTION:MEDICINE_RECOGNITION]"""


        # ===== FEATURE SUGGESTION: BOOK APPOINTMENT =====
    if any(phrase in msg for phrase in [
        'book an appointment',
        'book appointment',
        'schedule an appointment',
        'schedule appointment',
        'make an appointment',
        'make appointment',
        'appointment with a doctor',
        'doctor appointment',
        'book a consultation',
        'book consultation',
        'schedule a consultation',
        'schedule consultation',
        'need an appointment',
        'want an appointment'
    ]):
        return """📅 **Book Appointment**

You can book a consultation with an available doctor through OpenHealth.

[ACTION:BOOK_APPOINTMENT]"""


        # ===== FEATURE SUGGESTION: DISEASE PREDICTION =====
    if any(phrase in msg for phrase in [
        'predict my disease',
        'predict a disease',
        'disease prediction',
        'predict disease',
        'check my disease risk',
        'check disease risk',
        'check my health risk',
        'health risk prediction',
        'disease risk prediction',
        'can you predict my disease',
        'can i predict my disease',
        'want to predict a disease',
        'want disease prediction',
        'check if i have a disease'
    ]):
        return """❤️ **Disease Prediction**

OpenHealth provides AI-powered disease prediction tools that can help you assess risk for supported health conditions.

[ACTION:DISEASE_PREDICTION]"""


    if any(word in msg for word in ['symptom', 'symptoms', 'warning signs']):
        return """📋 **Common Symptoms Guide**

**🔴 When to See a Doctor:**
• Unexplained weight loss
• Persistent fever (3+ days)
• Severe headache
• Chest pain
• Difficulty breathing
• Unusual bleeding
• Changes in vision
• Severe abdominal pain
• Prolonged fatigue

⚠️ **Always consult a doctor for proper diagnosis!**"""

        # ===== GENERAL WELLNESS: DIET & NUTRITION =====
    if any(word in msg for word in [
        'nutrition',
        'diet',
        'healthy diet',
        'healthy eating',
        'healthy food',
        'healthy foods',
        'balanced diet',
        'balanced meal',
        'what should i eat',
        'what to eat',
        'good food',
        'nutrients',
        'nutrition tips'
    ]):
        return """🥗 **Diet & Nutrition Basics**

A healthy diet generally includes a variety of vegetables, fruits, whole grains, protein-rich foods, and healthy fats.

**🍎 Simple Tips:**
• Eat a variety of fruits and vegetables
• Choose whole grains when possible
• Include protein-rich foods in your meals
• Drink enough fluids throughout the day
• Limit highly processed foods and excess added sugar
• Keep your meals balanced and varied

**🥗 Simple Meal Idea:**
Try combining vegetables + a protein source + whole grains for a balanced meal.

💡 **Small, consistent healthy choices are more useful than extreme diets.**

⚠️ **For a medical condition or a personalized diet plan, consult a qualified healthcare professional or registered dietitian.**"""


        # ===== GENERAL WELLNESS: YOGA =====
    if any(phrase in msg for phrase in [
        'yoga',
        'yoga benefits',
        'benefits of yoga',
        'yoga for health',
        'yoga exercises',
        'yoga exercise',
        'yoga poses',
        'yoga for beginners',
        'beginner yoga',
        'simple yoga'
    ]):
        return """🧘‍♀️ **Yoga & Wellness Basics**

Yoga combines physical postures, breathing practices, and mindfulness.

**🌿 General Benefits:**
• Can support flexibility and balance
• Can help with relaxation and stress management
• May support body awareness
• Can be part of a regular physical activity routine
• Breathing and mindfulness practices may promote relaxation

**🧘‍♀️ Beginner Tips:**
• Start with simple, comfortable movements
• Focus on controlled breathing
• Don't force a stretch or posture
• Practice on a stable, comfortable surface
• Start gradually and increase activity as you become comfortable

💡 **Consistency is more important than doing difficult poses.**

⚠️ **If you have an injury, medical condition, or pain during exercise, seek appropriate professional guidance.**"""


        # ===== GENERAL WELLNESS: EXERCISE =====
    if any(phrase in msg for phrase in [
        'exercise',
        'exercises',
        'physical activity',
        'workout',
        'workouts',
        'fitness',
        'fitness tips',
        'exercise benefits',
        'benefits of exercise',
        'how much exercise',
        'daily exercise',
        'regular exercise',
        'beginner exercise',
        'beginner workout',
        'home workout',
        'home exercise'
    ]):
        return """🏃‍♀️ **Exercise & Fitness Basics**

Regular physical activity can support overall health, fitness, strength, and well-being.

**💪 Simple Tips:**
• Start with activities you enjoy, such as walking, cycling, or light exercise
• Begin gradually if you are new to exercise
• Include a mix of aerobic activity and strength-building activities
• Take breaks and allow your body time to recover
• Stay hydrated during physical activity
• Try to make movement a regular part of your day

**🚶 Easy Ways to Stay Active:**
• Take a walk
• Use stairs when comfortable
• Stretch during breaks
• Try beginner-friendly exercises at home
• Spend less time sitting continuously

💡 **You don't need an intense workout to start being active. Consistency matters.**

⚠️ **If you have a medical condition, injury, or experience pain, dizziness, or unusual shortness of breath during exercise, stop and seek appropriate medical advice.**"""

        # ===== GENERAL WELLNESS: SLEEP =====
    if any(phrase in msg for phrase in [
        'sleep',
        'sleeping',
        'sleep health',
        'sleep tips',
        'better sleep',
        'improve sleep',
        'how to sleep',
        'sleep better',
        'sleep problems',
        'sleep routine',
        'sleep schedule',
        'healthy sleep',
        'good sleep'
    ]):
        return """😴 **Sleep & Wellness Basics**

Good sleep is an important part of overall health and well-being.

**🌙 Simple Sleep Tips:**
• Try to keep a consistent sleep and wake schedule
• Create a quiet and comfortable sleep environment
• Reduce bright screens and stimulating activities before bedtime
• Avoid heavy meals and excessive caffeine close to bedtime
• Give yourself enough time to sleep
• Use a relaxing bedtime routine such as reading or gentle breathing

**🛏️ Healthy Sleep Routine:**
A regular bedtime routine can help your body and mind prepare for sleep.

💡 **Small changes to your daily routine can help support better sleep.**

⚠️ **If sleep problems are persistent, severe, or affecting your daily life, consider speaking with a healthcare professional.**"""


        # ===== GENERAL WELLNESS: HYDRATION =====
    if any(phrase in msg for phrase in [
        'hydration',
        'hydrated',
        'drink water',
        'drinking water',
        'water intake',
        'how much water',
        'how much water should i drink',
        'water for health',
        'stay hydrated',
        'stay hydrated',
        'hydration tips'
    ]):
        return """💧 **Hydration & Wellness Basics**

Staying adequately hydrated helps your body function normally and supports everyday health.

**💧 Simple Hydration Tips:**
• Drink water regularly throughout the day
• Keep water available when you are working or travelling
• Drink more fluids when you are physically active or sweating
• Include water-rich foods such as fruits and vegetables
• Pay attention to thirst and your body's hydration needs

**🥤 Easy Habit:**
Keep a reusable water bottle nearby so drinking water becomes part of your daily routine.

💡 **Your fluid needs can vary depending on activity, weather, diet, and individual health circumstances.**

⚠️ **If you have a medical condition that affects how much fluid you should drink, follow the advice of your healthcare professional.**"""

        # ===== GENERAL WELLNESS: STRESS MANAGEMENT =====
    if any(phrase in msg for phrase in [
        'stress',
        'stressed',
        'stress management',
        'manage stress',
        'reduce stress',
        'how to reduce stress',
        'stress relief',
        'relieve stress',
        'relaxation',
        'relax',
        'feeling stressed',
        'stress tips',
        'calm down'
    ]):
        return """🧘 **Stress Management & Wellness Basics**

Some everyday habits can help support relaxation and manage normal day-to-day stress.

**🌿 Simple Tips:**
• Take slow, comfortable breaths
• Try gentle stretching or yoga
• Go for a walk or spend some time outdoors
• Keep a regular sleep routine
• Take short breaks when you feel overwhelmed
• Talk with someone you trust
• Make time for activities you enjoy

**🧘 Quick Relaxation Idea:**
Take a few slow breaths, relax your shoulders, and give yourself a short break from the activity you are doing.

💡 **Different strategies work for different people. Find a routine that feels comfortable and sustainable for you.**

⚠️ **If stress is persistent, overwhelming, or interfering significantly with daily life, consider speaking with a qualified healthcare professional.**"""


    if any(word in msg for word in ['emergency', '911', 'urgent', 'immediate']):
        return """🚨 **EMERGENCY INFORMATION**

**📞 Call Emergency Services Immediately:**
• Chest pain/pressure
• Difficulty breathing
• Severe bleeding
• Loss of consciousness
• Seizures
• Head injury
• Stroke symptoms
• Severe allergic reaction

**🚨 Stroke Signs (FAST):**
• **F**ace drooping
• **A**rm weakness
• **S**peech difficulty
• **T**ime to call 911!

⚠️ **DO NOT WAIT - Call emergency services NOW!**

📱 **Emergency Number:**
• India: 102/108
• USA: 911
• UK: 999"""

    return """💡 **I'm your Health Assistant!**

I can provide detailed information about:
• 💉 Diabetes
• ❤️ Heart Disease
• 🎀 Breast Cancer
• 🧪 Liver Disease
• 🫘 Kidney Disease

**Ask me about:**
• Symptoms & Warning Signs
• Risk Factors
• Prevention Tips
• Treatment Options
• Nutrition & Diet

⚠️ **Disclaimer:** I'm an AI assistant, not a doctor. Always consult a healthcare professional!"""