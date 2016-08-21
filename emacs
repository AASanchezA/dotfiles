;; Essential settings.
(setq inhibit-splash-screen t
      inhibit-startup-message t
      inhibit-startup-echo-area-message t)
;;To be remove
(menu-bar-mode 1)
(tool-bar-mode -1)
(when (boundp 'scroll-bar-mode)
  (scroll-bar-mode -1))
(show-paren-mode 1)
(setq visual-line-fringe-indicators '(left-curly-arrow right-curly-arrow))
(setq-default left-fringe-width nil)
(setq-default indent-tabs-mode nil)
(eval-after-load "vc" '(setq vc-handled-backends nil))
(setq vc-follow-symlinks t)
(setq large-file-warning-threshold nil)
(setq split-width-threshold nil)
(setq custom-safe-themes t)
(put 'narrow-to-region 'disabled nil)
(setq-default tab-width 4) ; or any other preferred value
(setq whitespace-style '(trailing tabs newline tab-mark newline-mark))

;;Set Package repos
(require 'package)
(add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/"))
(add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/"))
(add-to-list 'package-archives '("melpa-stable" . "http://stable.melpa.org/packages/"))

(setq package-enable-at-startup nil)
(package-initialize)

(defun ensure-package-installed (&rest packages)
    "Assure every package is installed, ask for installation if it’s not.

	Return a list of installed packages or nil for every skipped package."
	(mapcar
		(lambda (package)
			(if (package-installed-p package)
				nil
				(if (y-or-n-p (format "Package %s is missing. Install it? " package))
					(package-install package)
				package)))
		packages))

;; Make sure to have downloaded archive description.
(or (file-exists-p package-user-dir)
	    (package-refresh-contents))

;; Activate installed packages
(package-initialize)

;; Assuming you wish to install 
(ensure-package-installed 'helm 'evil 'projectile 'powerline 'magit)

(load-theme 'monokai t)

(require 'helm)
(global-set-key (kbd "M-x") 'helm-M-x)
(global-set-key (kbd "C-x C-f") 'helm-find-files)

(require 'evil)
(evil-mode t)
;(define-key evil-insert-state-map "ii" 'evil-normal-state)

(require 'powerline)
(powerline-center-evil-theme)

