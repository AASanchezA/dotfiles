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
(ensure-package-installed 'helm 'helm-projectile)
(ensure-package-installed 'powerline 'monokai-theme)
(ensure-package-installed 'evil 'evil-leader 'evil-nerd-commenter)
(ensure-package-installed 'evil-tabs)
(ensure-package-installed 'key-chord 'auto-complete)
(ensure-package-installed 'flycheck)
(ensure-package-installed 'elpy)
;; (ensure-package-installed 'speed-type)

(load-theme 'monokai t)
(server-start)

(require 'helm)
(require 'helm-config)
(global-set-key (kbd "M-x") 'helm-M-x)
(global-set-key (kbd "C-x C-f") 'helm-find-files)

;; The default "C-x c" is quite close to "C-x C-c", which quits Emacs.
;; Changed to "C-c h". Note: We must set "C-c h" globally, because we
;; cannot change `helm-command-prefix-key' once `helm-config' is loaded.
(global-set-key (kbd "C-c h") 'helm-command-prefix)
(global-unset-key (kbd "C-x c"))

(define-key helm-map (kbd "<tab>") 'helm-execute-persistent-action) ; rebind tab to run persistent action
(define-key helm-map (kbd "C-i") 'helm-execute-persistent-action) ; make TAB work in terminal
(define-key helm-map (kbd "C-z")  'helm-select-action) ; list actions using C-z

(when (executable-find "curl")
  (setq helm-google-suggest-use-curl-p t))

(setq helm-split-window-in-side-p           t ; open helm buffer inside current window, not occupy whole other window
      helm-move-to-line-cycle-in-source     t ; move to end or beginning of source when reaching top or bottom of source.
      helm-ff-search-library-in-sexp        t ; search for library in `require' and `declare-function' sexp.
      helm-scroll-amount                    8 ; scroll 8 lines other window using M-<next>/M-<prior>
      helm-ff-file-name-history-use-recentf t)

(helm-mode 1)

;; Vim key bindings
(require 'evil-leader)
(evil-leader/set-leader ",")
(global-evil-leader-mode)
(evil-leader/set-key
  "cc" 'evilnc-comment-or-uncomment-lines
  "cu" 'evilnc-comment-or-uncomment-lines
  ;; "cl" 'evilnc-quick-comment-or-uncomment-to-the-line
  ;; "ll" 'evilnc-quick-comment-or-uncomment-to-the-line
  ;; "cc" 'evilnc-copy-and-comment-lines
  ;; "cp" 'evilnc-comment-or-uncomment-paragraphs
  ;; "cr" 'comment-or-uncomment-region
  ;; "cv" 'evilnc-toggle-invert-comment-line-by-line
  "\\" 'evilnc-comment-operator ; if you prefer backslash key
)

(setq evil-emacs-state-cursor '("red" box))
(setq evil-normal-state-cursor '("green" box))
(setq evil-visual-state-cursor '("orange" box))
(setq evil-insert-state-cursor '("red" bar))
(setq evil-replace-state-cursor '("red" bar))
(setq evil-operator-state-cursor '("red" hollow))

(require 'evil)
(evil-mode t)
(global-evil-tabs-mode t)

(require 'key-chord)
(setq key-chord-two-keys-delay 0.5)
(key-chord-define evil-insert-state-map "ii" 'evil-normal-state)
(key-chord-mode 1)

(require 'powerline)
(powerline-center-evil-theme)

;;Autocomplete and fly
(ac-config-default)
(global-flycheck-mode)

;; Elpy Settings
(elpy-enable)
;; (elpy-use-ipython)
(setq elpy-rpc-backend "jedi")

;;BackUp Files
(setq backup-directory-alist
        `((".*" . ,temporary-file-directory)))
(setq auto-save-file-name-transforms
        `((".*" ,temporary-file-directory t)))

;(message "Deleting old backup files...")
;(let ((week (* 60 60 24 7))
      ;(current (float-time (current-time))))
  ;(dolist (file (directory-files temporary-file-directory t))
    ;(when (and (backup-file-name-p file)
               ;(> (- current (float-time (fifth (file-attributes file))))
                  ;week))
      ;(message "%s" file)
      ;(delete-file file))))

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
   (quote
    (evil-nerd-commenter magit powerline projectile monokai-theme helm evil)))
 '(show-paren-mode t)
 '(size-indication-mode t)
 '(tool-bar-mode nil))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:family "Ubuntu Mono" :foundry "outline" :slant normal :weight normal :height 120 :width normal)))))
(put 'erase-buffer 'disabled nil)
