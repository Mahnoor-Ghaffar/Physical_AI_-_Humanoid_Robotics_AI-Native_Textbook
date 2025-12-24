import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useThemeConfig } from '@docusaurus/theme-common';
import { useBaseUrl } from '@docusaurus/useBaseUrl';
import styles from './CustomFooter.module.css';

function FooterLink({ to, href, label, prependBaseUrlToHref, ...props }) {
  const toUrl = useBaseUrl(to);
  const normalizedHref = useBaseUrl(href, { forcePrependBaseUrl: true });
  return (
    <Link
      className={styles.footerLink}
      {...(href
        ? {
            href: prependBaseUrlToHref ? normalizedHref : href,
          }
        : {
            to: toUrl,
          })}
      {...props}>
      {label}
    </Link>
  );
}

const FooterLogo = ({ logo, alt }) => (
  <div className="footer__logo">
    <img className="footer__logo-image" src={useBaseUrl(logo)} alt={alt} />
  </div>
);

function CustomFooter() {
  const { footer } = useThemeConfig();

  const { copyright, links = [], logo } = footer || {};

  if (!footer) {
    return null;
  }

  // Process copyright to highlight author name
  const processedCopyright = copyright ? copyright.replace(
    'Mahnoor Ghaffar',
    '<span class="footer__author">Mahnoor Ghaffar</span>'
  ) : '';

  return (
    <footer className={clsx('footer', styles.customFooter)}>
      <div className="container container-fluid">
        {logo && logo.src && <FooterLogo {...logo} />}
        {links && links.length > 0 && (
          <div className="row footer__links">
            {links.map((linkItem, i) => (
              <div key={i} className="col footer__col">
                {linkItem.title != null ? (
                  <h4 className={styles.footer__title}>{linkItem.title}</h4>
                ) : null}
                {linkItem.items != null &&
                Array.isArray(linkItem.items) &&
                linkItem.items.length > 0 ? (
                  <ul className={styles.footer__items}>
                    {linkItem.items.map((item, key) => (
                      <li key={key} className={styles.footer__item}>
                        <FooterLink {...item} />
                      </li>
                    ))}
                  </ul>
                ) : null}
              </div>
            ))}
          </div>
        )}
        {(logo || copyright) && (
          <div className="footer__bottom text--center">
            {copyright ? (
              <div
                className={styles.footer__copyright}
                dangerouslySetInnerHTML={{
                  __html: processedCopyright,
                }}
              />
            ) : null}
          </div>
        )}
      </div>
    </footer>
  );
}

export default CustomFooter;