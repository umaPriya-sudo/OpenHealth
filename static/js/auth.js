/* =========================================================
   OpenHealth Authentication
   Modal + Sign In + Sign Up + Logout
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const authModal = document.getElementById("authModal");

    if (!authModal) {
        return;
    }

    const signInForm = document.getElementById("signInForm");
    const signUpForm = document.getElementById("signUpForm");

    const signInTab = document.getElementById("signInTab");
    const signUpTab = document.getElementById("signUpTab");

    const authMessage = document.getElementById("authMessage");

    const closeButtons = document.querySelectorAll("[data-auth-close]");

    /* =====================================================
       Open Modal
       ===================================================== */

    function openAuthModal(mode = "signin") {

        authModal.classList.add("is-open");
        authModal.setAttribute("aria-hidden", "false");

        document.body.classList.add("auth-modal-open");

        clearMessage();

        switchAuthMode(mode);

        const firstInput =
            mode === "signup"
                ? document.getElementById("signupFullName")
                : document.getElementById("signinEmail");

        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }


    /* =====================================================
       Close Modal
       ===================================================== */

    function closeAuthModal() {

        authModal.classList.remove("is-open");
        authModal.setAttribute("aria-hidden", "true");

        document.body.classList.remove("auth-modal-open");

        clearMessage();
    }


    /* =====================================================
       Switch Sign In / Sign Up
       ===================================================== */

    function switchAuthMode(mode) {

        clearMessage();

        if (mode === "signup") {

            signInForm.classList.remove("active");
            signUpForm.classList.add("active");

            signInTab.classList.remove("active");
            signUpTab.classList.add("active");

        } else {

            signUpForm.classList.remove("active");
            signInForm.classList.add("active");

            signUpTab.classList.remove("active");
            signInTab.classList.add("active");
        }
    }


    /* =====================================================
       Authentication Message
       ===================================================== */

    function showMessage(message, type = "error") {

        authMessage.textContent = message;

        authMessage.className =
            `auth-message show ${type}`;
    }


    function clearMessage() {

        authMessage.textContent = "";

        authMessage.className = "auth-message";
    }


    /* =====================================================
       Close Buttons
       ===================================================== */

    closeButtons.forEach(button => {

        button.addEventListener("click", closeAuthModal);

    });


    /* =====================================================
       Tabs
       ===================================================== */

    signInTab.addEventListener("click", () => {

        switchAuthMode("signin");

    });


    signUpTab.addEventListener("click", () => {

        switchAuthMode("signup");

    });


    /* =====================================================
       Switch Links
       ===================================================== */

    document
        .querySelectorAll("[data-auth-switch]")
        .forEach(button => {

            button.addEventListener("click", () => {

                const mode =
                    button.getAttribute("data-auth-switch");

                switchAuthMode(mode);

            });

        });


    /* =====================================================
       Password Show / Hide
       ===================================================== */

    document
        .querySelectorAll("[data-password-toggle]")
        .forEach(button => {

            button.addEventListener("click", () => {

                const inputId =
                    button.getAttribute(
                        "data-password-toggle"
                    );

                const input =
                    document.getElementById(inputId);

                const icon =
                    button.querySelector("i");

                if (!input) {
                    return;
                }

                if (input.type === "password") {

                    input.type = "text";

                    icon.classList.remove("fa-eye");
                    icon.classList.add("fa-eye-slash");

                    button.setAttribute(
                        "aria-label",
                        "Hide password"
                    );

                } else {

                    input.type = "password";

                    icon.classList.remove("fa-eye-slash");
                    icon.classList.add("fa-eye");

                    button.setAttribute(
                        "aria-label",
                        "Show password"
                    );
                }
            });

        });


    /* =====================================================
       SIGN UP
       ===================================================== */

    signUpForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        clearMessage();

        /* -----------------------------------------
           Common fields
           ----------------------------------------- */

        const fullName =
            document
                .getElementById("signupFullName")
                .value
                .trim();

        const email =
            document
                .getElementById("signupEmail")
                .value
                .trim();

        const password =
            document
                .getElementById("signupPassword")
                .value;

        const confirmPassword =
            document
                .getElementById("signupConfirmPassword")
                .value;

        const termsAccepted =
            document
                .getElementById("termsAccepted")
                .checked;


        /* -----------------------------------------
           Account Type
           ----------------------------------------- */

        const selectedAccountType =
            document.querySelector(
                'input[name="account_type"]:checked'
            );

        if (!selectedAccountType) {

            showMessage(
                "Please select Patient or Doctor."
            );

            return;
        }

        const accountType =
            selectedAccountType.value;


        /* -----------------------------------------
           Common validation
           ----------------------------------------- */

        if (!fullName) {

            showMessage(
                "Please enter your full name."
            );

            return;
        }


        if (!email) {

            showMessage(
                "Please enter your email address."
            );

            return;
        }


        if (password.length < 8) {

            showMessage(
                "Password must be at least 8 characters."
            );

            return;
        }


        if (password !== confirmPassword) {

            showMessage(
                "Passwords do not match."
            );

            return;
        }


        if (!termsAccepted) {

            showMessage(
                "Please accept the Terms of Service and Privacy Policy."
            );

            return;
        }


        /* -----------------------------------------
           Create request data
           ----------------------------------------- */

        const signupData = {
            account_type: accountType,
            full_name: fullName,
            email: email,
            password: password
        };


        /* -----------------------------------------
           Doctor-specific fields
           ----------------------------------------- */

        if (accountType === "doctor") {

            const registrationNumber =
                document
                    .getElementById("doctorRegistrationNumber")
                    .value
                    .trim();

            const qualification =
                document
                    .getElementById("doctorQualification")
                    .value
                    .trim();

            const specialization =
                document
                    .getElementById("doctorSpecialization")
                    .value;

            const experienceYears =
                document
                    .getElementById("doctorExperience")
                    .value;

            const bio =
                document
                    .getElementById("doctorBio")
                    .value
                    .trim();

            const clinicName =
                document
                    .getElementById("doctorClinicName")
                    .value
                    .trim();

            const clinicAddress =
                document
                    .getElementById("doctorClinicAddress")
                    .value
                    .trim();

            const city =
                document
                    .getElementById("doctorCity")
                    .value
                    .trim();

            const consultationFee =
                document
                    .getElementById("doctorConsultationFee")
                    .value;


            /* Consultation types */

            const consultationTypes =
                Array.from(
                    document.querySelectorAll(
                        'input[name="consultation_type"]:checked'
                    )
                ).map(
                    checkbox => checkbox.value
                );


            signupData.registration_number =
                registrationNumber;

            signupData.qualification =
                qualification;

            signupData.specialization =
                specialization;

            signupData.experience_years =
                experienceYears;

            signupData.bio =
                bio;

            signupData.clinic_name =
                clinicName;

            signupData.clinic_address =
                clinicAddress;

            signupData.city =
                city;

            signupData.consultation_fee =
                consultationFee;

            signupData.consultation_type =
                consultationTypes;
        }


        /* -----------------------------------------
           Button loading state
           ----------------------------------------- */

        const button =
            document.getElementById("signUpBtn");

        const originalText =
            button.innerHTML;

        button.disabled = true;

        button.innerHTML =
            accountType === "doctor"
                ? `<span>Registering...</span>`
                : `<span>Creating account...</span>`;


        /* -----------------------------------------
           Send signup request
           ----------------------------------------- */

        try {

            const response =
                await fetch("/api/auth/signup", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "same-origin",

                    body: JSON.stringify(
                        signupData
                    )
                });


            const data =
                await response.json();


            /* -----------------------------------------
               Error response
               ----------------------------------------- */

            if (!response.ok || !data.success) {

                showMessage(
                    data.message ||
                    "Unable to create account."
                );

                return;
            }


            /* -----------------------------------------
               Open Email Verification
            ----------------------------------------- */

            verificationUserId =
                data.user_id;

            verificationEmailAddress =
                email;

            const verificationSection =
                document.getElementById(
                    "emailVerificationSection"
                );
            
            const verificationEmail =
                document.getElementById(
                    "verificationEmail"
                );
            
            const verificationOtp =
                document.getElementById(
                    "verificationOtp"
                );
            
            
            if (
                verificationSection &&
                verificationEmail
            ) {
            
                verificationEmail.textContent =
                    email;
            
                verificationSection.classList.add(
                    "show"
                );
            
                signUpForm
                    .querySelectorAll(
                        ":scope > *"
                    )
                    .forEach((element) => {
                    
                        if (
                            element.id !==
                            "emailVerificationSection"
                        ) {
                            element.style.display = "none";
                        }
                    
                    });
                
                if (verificationOtp) {
                
                    verificationOtp.value = "";
                
                    setTimeout(() => {
                    
                        verificationOtp.focus();
                    
                    }, 100);
                
                }
            
            }


        } catch (error) {

            console.error(
                "Sign up error:",
                error
            );

            showMessage(
                "Something went wrong. Please try again."
            );

        } finally {

            button.disabled = false;

            button.innerHTML = originalText;
        }

    });

    /* =====================================================
       SIGN IN
       ===================================================== */

    signInForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        clearMessage();

        const email =
            document
                .getElementById("signinEmail")
                .value
                .trim();

        const password =
            document
                .getElementById("signinPassword")
                .value;


        if (!email || !password) {

            showMessage(
                "Please enter your email and password."
            );

            return;
        }


        const button =
            document.getElementById("signInBtn");

        const originalText =
            button.innerHTML;

        button.disabled = true;

        button.innerHTML =
            `<span>Signing in...</span>`;


        try {

            const response =
                await fetch("/api/auth/signin", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "same-origin",

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                showMessage(
                    data.message ||
                    "Invalid email or password."
                );

                return;
            }


            showMessage(
                "Signed in successfully.",
                "success"
            );


            /* Give the success message a moment */

            setTimeout(() => {
            
                closeAuthModal();
            
                // Redirect user based on account role
                const role = data.user?.role;
            
                if (role === "patient") {
                
                    window.location.href = "/patient/dashboard";
                
                } else if (role === "doctor") {
                
                    window.location.href = "/doctor/dashboard";
                
                } else {
                
                    window.location.href = "/";
                
                }
            
}, 600);


        } catch (error) {

            console.error(
                "Sign in error:",
                error
            );

            showMessage(
                "Something went wrong. Please try again."
            );

        } finally {

            button.disabled = false;

            button.innerHTML = originalText;
        }

    });


    /* =====================================================
       Forgot Password
       ===================================================== */

    document
        .getElementById("forgotPasswordBtn")
        .addEventListener("click", () => {

            showMessage(
                "Password recovery will be available soon.",
                "success"
            );

        });


    /* =====================================================
       Google Sign-In
       ===================================================== */

    document.querySelectorAll("#googleSignInBtn, #googleSignUpBtn").forEach(button => {
        button.addEventListener("click", () => {
            window.location.href = "/api/auth/google";
        });
    });


    /* ================================================= 
       Escape Key
       ===================================================== */

    document.addEventListener("keydown", (event) => {

        if (
            event.key === "Escape" &&
            authModal.classList.contains("is-open")
        ) {
            closeAuthModal();
        }

    });


    /* =====================================================
       Prevent Overlay Click From Affecting Card
       ===================================================== */

    const modalCard =
        document.querySelector(".auth-modal-card");

    if (modalCard) {

        modalCard.addEventListener(
            "click",
            event => event.stopPropagation()
        );

    }

    /* =====================================================
   EMAIL VERIFICATION
   ===================================================== */

const verifyEmailBtn =
    document.getElementById(
        "verifyEmailBtn"
    );

const resendVerificationBtn =
    document.getElementById(
        "resendVerificationBtn"
    );

const verificationBackBtn =
    document.getElementById(
        "verificationBackBtn"
    );

const verificationOtpInput =
    document.getElementById(
        "verificationOtp"
    );

let verificationUserId = null;
let verificationEmailAddress = null;


/* -----------------------------------------
   Verify Email
   ----------------------------------------- */

if (verifyEmailBtn) {

    verifyEmailBtn.addEventListener(
        "click",
        async () => {

            clearMessage();

            const otp =
                verificationOtpInput
                    ?.value
                    .trim();


            if (!verificationUserId) {

                showMessage(
                    "Verification session expired. Please sign up again."
                );

                return;
            }


            if (
                !otp ||
                !/^\d{6}$/.test(otp)
            ) {

                showMessage(
                    "Please enter a valid 6-digit verification code."
                );

                return;
            }


            const originalText =
                verifyEmailBtn.innerHTML;

            verifyEmailBtn.disabled = true;

            verifyEmailBtn.innerHTML =
                `<span>Verifying...</span>`;


            try {

                const response =
                    await fetch(
                        "/api/auth/verify-email",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            credentials:
                                "same-origin",

                            body: JSON.stringify({
                                user_id:
                                    verificationUserId,
                                otp: otp
                            })

                        }
                    );


                const data =
                    await response.json();


                if (
                    !response.ok ||
                    !data.success
                ) {

                    showMessage(
                        data.message ||
                        "Unable to verify email."
                    );

                    return;
                }


                showMessage(
                    "Email verified successfully. You can now sign in.",
                    "success"
                );


                setTimeout(() => {

                    switchAuthMode(
                        "signin"
                    );

                    const signinEmail =
                        document.getElementById(
                            "signinEmail"
                        );

                    const signinPassword =
                        document.getElementById(
                            "signinPassword"
                        );


                    if (signinEmail) {

                        signinEmail.value =
                            verificationEmailAddress ||
                            "";
                    }


                    if (signinPassword) {

                        signinPassword.value =
                            "";

                        signinPassword.focus();
                    }


                    resetVerificationState();

                }, 1000);


            } catch (error) {

                console.error(
                    "Email verification error:",
                    error
                );

                showMessage(
                    "Something went wrong. Please try again."
                );

            } finally {

                verifyEmailBtn.disabled =
                    false;

                verifyEmailBtn.innerHTML =
                    originalText;
            }

        }
    );

}

/* -----------------------------------------
   Resend Verification Code
   ----------------------------------------- */

if (resendVerificationBtn) {

    resendVerificationBtn.addEventListener(
        "click",
        async () => {

            clearMessage();

            if (
                !verificationUserId ||
                !verificationEmailAddress
            ) {

                showMessage(
                    "Verification session expired. Please sign up again."
                );

                return;
            }

            const originalText =
                resendVerificationBtn.textContent;

            resendVerificationBtn.disabled = true;

            resendVerificationBtn.textContent =
                "Sending...";

            try {

                const response =
                    await fetch(
                        "/api/auth/resend-verification",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            credentials:
                                "same-origin",

                            body: JSON.stringify({
                                user_id:
                                    verificationUserId,

                                email:
                                    verificationEmailAddress
                            })
                        }
                    );

                const data =
                    await response.json();

                if (
                    !response.ok ||
                    !data.success
                ) {

                    showMessage(
                        data.message ||
                        "Unable to resend verification code."
                    );

                    return;
                }

                showMessage(
                    "A new verification code has been sent to your email.",
                    "success"
                );

                if (verificationOtpInput) {

                    verificationOtpInput.value = "";

                    verificationOtpInput.focus();

                }

            } catch (error) {

                console.error(
                    "Resend verification error:",
                    error
                );

                showMessage(
                    "Something went wrong. Please try again."
                );

            } finally {

                resendVerificationBtn.disabled =
                    false;

                resendVerificationBtn.textContent =
                    originalText;
            }

        }
    );

}

/* -----------------------------------------
   OTP Input
   ----------------------------------------- */

if (verificationOtpInput) {

    verificationOtpInput.addEventListener(
        "input",
        () => {

            verificationOtpInput.value =
                verificationOtpInput.value
                    .replace(/\D/g, "")
                    .slice(0, 6);

        }
    );

}


/* -----------------------------------------
   Back Button
   ----------------------------------------- */

if (verificationBackBtn) {

    verificationBackBtn.addEventListener(
        "click",
        () => {

            resetVerificationState();

            clearMessage();

        }
    );

}


/* -----------------------------------------
   Reset Verification State
   ----------------------------------------- */

function resetVerificationState() {

    const verificationSection =
        document.getElementById(
            "emailVerificationSection"
        );


    if (verificationSection) {

        verificationSection.classList.remove(
            "show"
        );

    }


    signUpForm
        .querySelectorAll(
            ":scope > *"
        )
        .forEach((element) => {

            if (
                element.id !==
                "emailVerificationSection"
            ) {

                element.style.display = "";

            }

        });


    if (verificationOtpInput) {

        verificationOtpInput.value = "";

    }


    verificationUserId = null;

    verificationEmailAddress = null;
}

    window.openAuthModal = openAuthModal;
    window.closeAuthModal = closeAuthModal;

});

// ============================================================
// BREAST CANCER AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const breastCancerForm = document.getElementById("breastCancerForm");

    if (!breastCancerForm) {
        return;
    }

    breastCancerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        try {

            const response = await fetch("/api/auth/status", {
                method: "GET",
                credentials: "same-origin"
            });

            const data = await response.json();

            if (data.authenticated) {

                // User is logged in → allow prediction
                breastCancerForm.submit();

            } else {

                // User is not logged in → open Sign In modal
                openAuthModal("signin");

            }

        } catch (error) {

            console.error("Authentication check failed:", error);

            openAuthModal("signin");
        }

    });

});

// ============================================================
// NAVBAR AUTHENTICATION STATE
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    checkNavbarAuth();

});


// ------------------------------------------------------------
// CHECK LOGIN STATUS
// ------------------------------------------------------------

async function checkNavbarAuth() {

    try {

        const response = await fetch("/api/auth/status", {
            method: "GET",
            credentials: "same-origin"
        });

        const data = await response.json();

        updateNavbar(data);

    } catch (error) {

        console.error("Navbar authentication check failed:", error);

    }

}


// ------------------------------------------------------------
// UPDATE NAVBAR
// ------------------------------------------------------------

function updateNavbar(data) {

    const loggedOutNav = document.getElementById("loggedOutNav");
    const loggedInNav = document.getElementById("loggedInNav");

    const navUserName = document.getElementById("navUserName");
    const dropdownUserName = document.getElementById("dropdownUserName");
    const dropdownUserEmail = document.getElementById("dropdownUserEmail");

    if (!loggedOutNav || !loggedInNav) {
        return;
    }


    if (data.authenticated) {

        // Hide Sign In / Get Started
        loggedOutNav.style.display = "none";

        // Show user menu
        loggedInNav.style.display = "flex";


        if (data.user) {

            const fullName = data.user.full_name || "Account";
            const email = data.user.email || "";

            navUserName.textContent = fullName;

            dropdownUserName.textContent = fullName;

            dropdownUserEmail.textContent = email;

        }

    } else {

        // Show Sign In / Get Started
        loggedOutNav.style.display = "flex";

        // Hide user menu
        loggedInNav.style.display = "none";

    }

}

// ============================================================
// UPDATE NAVBAR IMMEDIATELY AFTER LOGIN
// ============================================================

window.addEventListener("openhealth:login", function () {
    checkNavbarAuth();
});


// ------------------------------------------------------------
// USER DROPDOWN
// ------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

    const userMenuButton = document.getElementById("userMenuButton");
    const userDropdown = document.getElementById("userDropdown");

    if (!userMenuButton || !userDropdown) {
        return;
    }


    userMenuButton.addEventListener("click", function (event) {

        event.stopPropagation();

        userDropdown.classList.toggle("show");

    });


    document.addEventListener("click", function () {

        userDropdown.classList.remove("show");

    });

});


// ------------------------------------------------------------
// LOGOUT
// ------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

    const logoutButton = document.getElementById("logoutButton");

    if (!logoutButton) {
        return;
    }


    logoutButton.addEventListener("click", async function () {

        try {

            const response = await fetch("/api/auth/logout", {
                method: "POST",
                credentials: "same-origin"
            });

            const data = await response.json();

            if (data.success) {

                window.location.href = "/";

            }

        } catch (error) {

            console.error("Logout failed:", error);

        }

    });

});

// ============================================================
// HEART DISEASE AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const heartDiseaseForm = document.getElementById("heartDiseaseForm");

    if (!heartDiseaseForm) {
        return;
    }

    heartDiseaseForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        try {

            const response = await fetch("/api/auth/status", {
                method: "GET",
                credentials: "same-origin"
            });

            const data = await response.json();

            if (data.authenticated) {

                // User is logged in → allow prediction
                heartDiseaseForm.submit();

            } else {

                // User is logged out → open Sign In modal
                openAuthModal("signin");

            }

        } catch (error) {

            console.error("Authentication check failed:", error);

            openAuthModal("signin");
        }

    });

});

// ============================================================
// DIABETES AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const diabetesForm = document.getElementById("diabetesForm");

    if (!diabetesForm) {
        return;
    }

    diabetesForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        try {

            const response = await fetch("/api/auth/status", {
                method: "GET",
                credentials: "same-origin"
            });

            const data = await response.json();

            if (data.authenticated) {

                // Logged in → allow prediction
                diabetesForm.submit();

            } else {

                // Logged out → open Sign In modal
                openAuthModal("signin");

            }

        } catch (error) {

            console.error("Authentication check failed:", error);

            openAuthModal("signin");
        }

    });

});

// ============================================================
// BRAIN TUMOR AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const brainTumorForm =
        document.getElementById("brainTumorForm");

    if (!brainTumorForm) {
        return;
    }

    brainTumorForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const response = await fetch(
                    "/api/auth/status",
                    {
                        method: "GET",
                        credentials: "same-origin"
                    }
                );

                const data = await response.json();

                if (data.authenticated) {

                    // Logged in → allow MRI analysis
                    brainTumorForm.submit();

                } else {

                    // Logged out → open Sign In modal
                    openAuthModal("signin");

                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                openAuthModal("signin");

            }

        }
    );

});

// ============================================================
// KIDNEY DISEASE AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const kidneyDiseaseForm =
        document.getElementById("kidneyDiseaseForm");

    if (!kidneyDiseaseForm) {
        return;
    }

    kidneyDiseaseForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const response = await fetch(
                    "/api/auth/status",
                    {
                        method: "GET",
                        credentials: "same-origin"
                    }
                );

                const data = await response.json();

                if (data.authenticated) {

                    // Logged in → allow kidney image analysis
                    kidneyDiseaseForm.submit();

                } else {

                    // Logged out → open Sign In modal
                    openAuthModal("signin");

                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                openAuthModal("signin");
            }

        }
    );

});

// ============================================================
// LIVER DISEASE AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const liverDiseaseForm =
        document.getElementById("liverDiseaseForm");

    if (!liverDiseaseForm) {
        return;
    }

    liverDiseaseForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const response = await fetch(
                    "/api/auth/status",
                    {
                        method: "GET",
                        credentials: "same-origin"
                    }
                );

                const data = await response.json();

                if (data.authenticated) {

                    // Logged in → allow liver prediction
                    liverDiseaseForm.submit();

                } else {

                    // Logged out → open Sign In modal
                    openAuthModal("signin");

                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                openAuthModal("signin");
            }

        }
    );

});

// ============================================================
// PARKINSON'S DISEASE AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const parkinsonsForm =
        document.getElementById("parkinsonsForm");

    if (!parkinsonsForm) {
        return;
    }

    parkinsonsForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const response = await fetch(
                    "/api/auth/status",
                    {
                        method: "GET",
                        credentials: "same-origin"
                    }
                );

                const data = await response.json();

                if (data.authenticated) {

                    // Logged in → allow prediction
                    parkinsonsForm.submit();

                } else {

                    // Logged out → open Sign In modal
                    openAuthModal("signin");

                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                openAuthModal("signin");
            }

        }
    );

});

// ============================================================
// MALARIA DETECTION AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const malariaForm =
        document.getElementById("malariaForm");

    if (!malariaForm) {
        return;
    }

    malariaForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            try {

                const response = await fetch(
                    "/api/auth/status",
                    {
                        method: "GET",
                        credentials: "same-origin"
                    }
                );

                const data = await response.json();

                if (data.authenticated) {

                    // Logged in → allow malaria detection
                    malariaForm.submit();

                } else {

                    // Logged out → open Sign In modal
                    openAuthModal("signin");

                }

            } catch (error) {

                console.error(
                    "Authentication check failed:",
                    error
                );

                openAuthModal("signin");
            }

        }
    );

});

// ============================================================
// MEDICINE RECOGNITION AUTHENTICATION CHECK
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    // --------------------------------------------------------
    // SEARCH MEDICINE BY NAME
    // --------------------------------------------------------

    const medicineSearchForm =
        document.getElementById("medicineSearchForm");

    if (medicineSearchForm) {

        medicineSearchForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();

                try {

                    const response = await fetch(
                        "/api/auth/status",
                        {
                            method: "GET",
                            credentials: "same-origin"
                        }
                    );

                    const data = await response.json();

                    if (data.authenticated) {

                        medicineSearchForm.submit();

                    } else {

                        openAuthModal("signin");

                    }

                } catch (error) {

                    console.error(
                        "Authentication check failed:",
                        error
                    );

                    openAuthModal("signin");
                }

            }
        );
    }


    // --------------------------------------------------------
    // IDENTIFY MEDICINE FROM IMAGE
    // --------------------------------------------------------

    const medicineUploadForm =
        document.getElementById("medicine-upload-form");

    if (medicineUploadForm) {

        medicineUploadForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();

                try {

                    const response = await fetch(
                        "/api/auth/status",
                        {
                            method: "GET",
                            credentials: "same-origin"
                        }
                    );

                    const data = await response.json();

                    if (data.authenticated) {

                        medicineUploadForm.submit();

                    } else {

                        openAuthModal("signin");

                    }

                } catch (error) {

                    console.error(
                        "Authentication check failed:",
                        error
                    );

                    openAuthModal("signin");
                }

            }
        );
    }

});

// =========================================
// SIGNUP ACCOUNT TYPE SELECTION
// =========================================

const accountTypeOptions =
    document.querySelectorAll(
        'input[name="account_type"]'
    );

const signupFields =
    document.getElementById("signupFields");

const doctorFields =
    document.getElementById("doctorFields");

const signUpBtn =
    document.getElementById("signUpBtn");

if (accountTypeOptions.length && signupFields) {

    accountTypeOptions.forEach((option) => {

        option.addEventListener("change", () => {

            // Show basic signup fields
            signupFields.classList.add("show");

            if (signUpBtn) {
                if (option.value === "doctor") {
                    signUpBtn.querySelector("span").textContent =
                        "Register as Doctor";
                } else {
                    signUpBtn.querySelector("span").textContent =
                        "Create Account";
                }
            }

            // Show / hide doctor-specific fields
            if (doctorFields) {

                if (option.value === "doctor") {
                    doctorFields.classList.add("show");
                } else {
                    doctorFields.classList.remove("show");
                }

            }

        });

    });

}

// =========================================
// DOCTOR TEXTAREA ICON BEHAVIOR
// =========================================

const doctorTextareas = document.querySelectorAll(
    ".doctor-textarea-wrapper textarea"
);

doctorTextareas.forEach((textarea) => {

    const icon = textarea
        .closest(".doctor-textarea-wrapper")
        ?.querySelector(":scope > i");

    if (!icon) return;

    const updateTextareaIcon = () => {

        if (
            document.activeElement === textarea ||
            textarea.value.trim() !== ""
        ) {
            icon.style.opacity = "0";
        } else {
            icon.style.opacity = "1";
        }

    };

    textarea.addEventListener(
        "focus",
        updateTextareaIcon
    );

    textarea.addEventListener(
        "blur",
        updateTextareaIcon
    );

    textarea.addEventListener(
        "input",
        updateTextareaIcon
    );

    updateTextareaIcon();
});

