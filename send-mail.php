<?php
header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

function clean_text($val) {
    return trim(strip_tags((string) $val));
}

$name    = clean_text($_POST['name'] ?? $_POST['fullName'] ?? 'Website Visitor');
$email   = filter_var(trim((string) ($_POST['email'] ?? '')), FILTER_SANITIZE_EMAIL);
$phone   = clean_text($_POST['phone'] ?? '');
$suburb  = clean_text($_POST['suburb'] ?? $_POST['address'] ?? '');
$service = clean_text($_POST['service'] ?? $_POST['projectType'] ?? 'Site Feasibility / Consultation');
$message = clean_text($_POST['message'] ?? $_POST['msg'] ?? '');

$to = 'admin@intellecthomes.com.au';
$subject = 'New Website Enquiry - ' . ($name !== '' ? $name : 'Intellect Homes');
$subject = str_replace(["\r", "\n"], '', $subject);

$bodyLines = [
    "New enquiry submitted via Intellect Homes website:",
    "--------------------------------------------------",
    "Name: " . ($name ?: 'N/A'),
    "Phone: " . ($phone ?: 'N/A'),
    "Email: " . ($email ?: 'N/A'),
    "Suburb / Address: " . ($suburb ?: 'N/A'),
    "Service / Interest: " . ($service ?: 'N/A'),
    "Message:",
    ($message ?: 'No additional message provided.'),
    "--------------------------------------------------",
    "Submitted at: " . date('Y-m-d H:i:s'),
];
$body = implode("\r\n", $bodyLines);

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: Intellect Homes Website <noreply@intellecthomes.com.au>',
];

if ($email && filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $safeEmail = str_replace(["\r", "\n"], '', $email);
    $headers[] = 'Reply-To: ' . $safeEmail;
}

$sent = @mail($to, $subject, $body, implode("\r\n", $headers));

echo json_encode([
    'success' => true,
    'mail_dispatched' => (bool) $sent,
    'message' => 'Thank you! Your enquiry has been received.'
]);
