# Auth lifecycle architecture (draft)

AuthN profiles emit a membership-verified signal. AuthZ grants live in
`wellmanifest/authority-lifecycle`. Commercial activation stays in
`wellmanifest/saas-lifecycle` under an onboarding profile such as
`membership-before-payment`.
