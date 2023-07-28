"use client";

import { DashboardSidebar } from "@/app/(dashboard)/DashboardSidebar";
import { makeStyles } from "@/lib/theme";
import { signOut } from "next-auth/react";
import { useState, useRef } from "react";

import { InfoMenu } from "@p4b/ui/components/InfoMenu";
import Footer from "@p4b/ui/components/Navigation/Footer";
import { Toolbar } from "@p4b/ui/components/Navigation/Toolbar";
import { Icon, Text, Button } from "@p4b/ui/components/theme";
import type { IconId } from "@p4b/ui/components/theme";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const { classes, cx } = useStyles();
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const ButtonElement = useRef(null);

  const handleClick = () => {
    setIsVisible(true);
  };
  const handleClose = () => {
    setIsVisible(false);
  };

  const menuHeader = (
    <span style={{ display: "flex", alignItems: "center" }}>
      <span style={{ marginRight: "5px" }}>
        <Icon iconId="coorperate" />
      </span>{" "}
      <Text typo="body 2">GOAT</Text>
    </span>
  );

  const actionHeader = (
    <Button startIcon="powerOff" onClick={() => signOut()}>
      Log Out
    </Button>
  );
  const items = [
    {
      link: "https://google.com",
      icon: () => (
        <>
          <div
            onClick={handleClick}
            ref={ButtonElement}
            style={{ padding: "3px 10px", borderRight: "2px solid #ccc" }}>
            <Icon iconId="user" size="medium" iconVariant="gray2" />
          </div>
          <InfoMenu
            ref={ButtonElement}
            handleCloseFunction={handleClose}
            status={isVisible}
            menuHeader={menuHeader}
            menuActions={actionHeader}>
            <Text typo="body 1">randomuser@outlook.com</Text>
            <Text typo="caption">Admin</Text>
          </InfoMenu>
        </>
      ),
    },
    {
      link: "https://google.com",
      icon: () => (
        <div style={{ padding: "3px 10px" }}>
          <Icon iconId="help" size="medium" iconVariant="gray2" />
        </div>
      ),
    },
  ];

  const sidebarItems: { link: string; icon: IconId; placeholder: string }[] = [
    {
      link: "/home",
      icon: "home",
      placeholder: "Home",
    },
    {
      link: "/content",
      icon: "folder",
      placeholder: "Content",
    },
    {
      link: "/settings",
      icon: "settings",
      placeholder: "Settings",
    },
    {
      link: "/help",
      icon: "help",
      placeholder: "Help",
    },
  ];

  const footerLinks: { header: string; links: { name: string; underline?: boolean; icon?: IconId }[] }[] = [
    {
      header: "Navigate",
      links: [
        {
          name: "Home it work",
        },
        {
          name: "Pricing",
        },
        {
          name: "Blog",
        },
        {
          name: "Demo",
        },
      ],
    },
    {
      header: "Study Areas",
      links: [
        {
          name: "Germany",
        },
        {
          name: "EU",
        },
        {
          name: "UK",
        },
        {
          name: "Asia",
        },
        {
          name: "Americas",
        },
      ],
    },
    {
      header: "Contact ",
      links: [
        {
          icon: "phone",
          name: "+49 89 2000 708 30",
          underline: true,
        },
        {
          icon: "email",
          name: "info@plan4better.de",
          underline: true,
        },
        {
          icon: "marker",
          name: "Am Kartoffelgarten 14 c/o WERK1 81671 München Germany",
          underline: true,
        },
      ],
    },
  ];

  return (
    <>
      <Toolbar height={52} items={items} />
      <DashboardSidebar items={sidebarItems} width={60} extended_width={200}>
        <div className={cx(classes.container)}>{children}</div>
      </DashboardSidebar>
      <Footer
        links={footerLinks}
        text="Lörem ipsum od ohet dilogi. Bell trabel, samuligt, ohöbel utom diska. Jinesade bel när feras redorade i belogi. FAR paratyp i muvåning, och pesask vyfisat. Viktiga poddradio har un mad och inde."
      />
    </>
  );
};

const useStyles = makeStyles({ name: { DashboardLayout } })(() => ({
  container: {
    minHeight: "100vh",
    margin: "0 auto",
    marginTop: "104px",
    width: "80%",
    "@media (max-width: 1714px)": {
      width: "90%",
    },
    "@media (max-width: 1500px)": {
      width: "90%",
    },
    "@media (max-width: 1268px)": {
      paddingLeft: "50px",
    },
  },
}));

export default DashboardLayout;
