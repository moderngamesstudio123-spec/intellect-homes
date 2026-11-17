<?php
$rootDir = realpath(__DIR__ . '/..');
$uriPath = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$uriPath = trim($uriPath, '/');

// Map legacy / old WordPress or .html paths cleanly
$aliasMap = [
    '' => 'index.php',
    'index.html' => 'index.php',
    'about.html' => 'about-us.php',
    'about-us' => 'about-us.php',
    'designs.html' => 'home-designs.php',
    'home-designs' => 'home-designs.php',
    'contact.html' => 'contact-us.php',
    'contact-us' => 'contact-us.php',
    'blog' => 'blogs.php',
];

if (isset($aliasMap[$uriPath])) {
    $uriPath = $aliasMap[$uriPath];
}

$candidate = $rootDir . '/' . $uriPath;
if (is_file($candidate) && pathinfo($candidate, PATHINFO_EXTENSION) === 'php') {
    $target = realpath($candidate);
} elseif (is_file($candidate . '.php')) {
    $target = realpath($candidate . '.php');
} else {
    $target = false;
}

if ($target && strpos($target, $rootDir) === 0 && is_file($target) && pathinfo($target, PATHINFO_EXTENSION) === 'php') {
    chdir(dirname($target));
    require $target;
} else {
    http_response_code(404);
    echo '404 - Page Not Found';
}
