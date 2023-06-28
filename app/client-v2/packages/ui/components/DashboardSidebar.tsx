import { Fade, List, ListItem, ListItemButton, ListItemIcon } from "@mui/material";
import { useState } from "react";

import { makeStyles } from "../lib/ThemeProvider";
import { Icon } from "./theme";
import type { IconId } from "./theme";
import { Text } from "./theme";
import { useTheme } from "./theme";

export type DashboardSidebarProps = {
  items: { link: string; icon: IconId; placeholder: string }[];
  width: number;
  extended_width: number;
  children: React.ReactNode;
};

export function DashboardSidebar(props: DashboardSidebarProps) {
  const { items, children } = props;
  const { classes, cx } = useStyles(props)();
  const theme = useTheme();
  console.log(theme);
  const [hover, setHover] = useState(false);
  const [active, setActive] = useState<string | null>(items[0].placeholder);

  const handleHover = () => {
    setHover((currHover) => !currHover);
  };

  return (
    <>
      <nav className={cx(classes.root)} onMouseEnter={handleHover} onMouseLeave={handleHover}>
        <List>
          {items?.map(({ link, icon, placeholder }, indx) => (
            <ListItem onClick={() => setActive(placeholder)} disablePadding key={indx}>
              <ListItemButton className={classes.itemList}>
                <ListItemIcon sx={{ marginRight: "10px" }}>
                  <Icon
                    size="default"
                    iconId={icon}
                    iconVariant={
                      active === placeholder ? "focus" : theme.isDarkModeEnabled ? "white" : "gray"
                    }
                  />
                </ListItemIcon>
                {hover ? (
                  <Fade in={true}>
                    <Text typo="body 2" color={active === placeholder ? "focus" : "primary"}>
                      {placeholder}
                    </Text>
                  </Fade>
                ) : (
                  <></>
                )}
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </nav>
      {children}
    </>
  );
}

const useStyles = (props: DashboardSidebarProps) =>
  makeStyles({ name: { DashboardSidebar } })((theme) => ({
    root: {
      backgroundColor: theme.colors.palette[theme.isDarkModeEnabled ? "dark" : "light"].light,
      cursor: "pointer",
      width: props.width,
      left: 0,
      top: 0,
      bottom: 0,
      position: "fixed",
      transition: "width 0.4s ease",
      display: "flex",
      flexDirection: "column",
      "&:hover": {
        width: props.extended_width,
      },
    },
    itemList: {
      "&:hover": {
        backgroundColor: theme.colors.palette[theme.isDarkModeEnabled ? "dark" : "light"].greyVariant1,
      },
    },
  }));