import { Router } from "express";
import { prisma } from "../../db/prisma.js";
import { asyncHandler } from "../../http/async-handler.js";
import { requireAuth } from "../../http/auth-middleware.js";
import { HttpError } from "../../http/errors.js";
import { requireParam } from "../../http/params.js";

export const projectRoutes = Router();

projectRoutes.use(requireAuth);

projectRoutes.get(
  "/",
  asyncHandler(async (req, res) => {
    const projects = await prisma.project.findMany({
      where: { memberships: { some: { userId: req.user!.sub } } },
      include: { documents: { orderBy: { updatedAt: "desc" } } },
      orderBy: { updatedAt: "desc" }
    });

    res.json({ projects });
  })
);

projectRoutes.post(
  "/",
  asyncHandler(async (req, res) => {
    const { name, description } = req.body as { name?: string; description?: string };
    if (!name?.trim()) {
      throw new HttpError(400, "Project name is required", "VALIDATION_ERROR");
    }

    const project = await prisma.project.create({
      data: {
        name: name.trim(),
        description: description?.trim(),
        memberships: {
          create: {
            userId: req.user!.sub,
            role: "OWNER"
          }
        },
        documents: {
          create: {
            title: "main.ts",
            language: "typescript",
            plainText: "export function hello(name: string) {\n  return `Hello, ${name}`;\n}\n"
          }
        }
      },
      include: { documents: true }
    });

    res.status(201).json({ project });
  })
);

projectRoutes.post(
  "/:projectId/documents",
  asyncHandler(async (req, res) => {
    const projectId = requireParam(req.params.projectId, "projectId");
    const { title, language, plainText } = req.body as {
      title?: string;
      language?: string;
      plainText?: string;
    };

    if (!title?.trim()) {
      throw new HttpError(400, "Document title is required", "VALIDATION_ERROR");
    }

    const membership = await prisma.projectMembership.findFirst({
      where: {
        projectId,
        userId: req.user!.sub,
        role: { in: ["OWNER", "EDITOR"] }
      },
      select: { id: true }
    });

    if (!membership) {
      throw new HttpError(404, "Project not found or read-only", "PROJECT_NOT_FOUND");
    }

    const document = await prisma.document.create({
      data: {
        projectId,
        title: title.trim(),
        language: language?.trim() || "typescript",
        plainText: plainText ?? ""
      }
    });

    res.status(201).json({ document });
  })
);
