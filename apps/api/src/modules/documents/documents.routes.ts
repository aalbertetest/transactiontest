import { Router } from "express";
import * as Y from "yjs";
import { prisma } from "../../db/prisma.js";
import { asyncHandler } from "../../http/async-handler.js";
import { requireAuth } from "../../http/auth-middleware.js";
import { HttpError } from "../../http/errors.js";
import { requireParam } from "../../http/params.js";

export const documentsRouter = Router();

documentsRouter.use(requireAuth);

documentsRouter.get(
  "/:documentId",
  asyncHandler(async (req, res) => {
    const documentId = requireParam(req.params.documentId, "documentId");
    const membership = await prisma.document.findFirst({
      where: {
        id: documentId,
        project: { memberships: { some: { userId: req.user!.sub } } }
      },
      include: { project: true }
    });

    if (!membership) {
      throw new HttpError(404, "Document not found", "DOCUMENT_NOT_FOUND");
    }

    res.json({
      document: {
        id: membership.id,
        projectId: membership.projectId,
        title: membership.title,
        language: membership.language,
        plainText: membership.plainText,
        version: membership.version,
        updatedAt: membership.updatedAt
      }
    });
  })
);

documentsRouter.patch(
  "/:documentId",
  asyncHandler(async (req, res) => {
    const documentId = requireParam(req.params.documentId, "documentId");
    const { title, language } = req.body as { title?: string; language?: string };
    const document = await prisma.document.findFirst({
      where: {
        id: documentId,
        project: { memberships: { some: { userId: req.user!.sub, role: { in: ["OWNER", "EDITOR"] } } } }
      }
    });

    if (!document) {
      throw new HttpError(404, "Document not found or read-only", "DOCUMENT_NOT_FOUND");
    }

    const updated = await prisma.document.update({
      where: { id: document.id },
      data: {
        title: title?.trim() ?? document.title,
        language: language?.trim() ?? document.language
      }
    });

    res.json({ document: updated });
  })
);

documentsRouter.get(
  "/:documentId/snapshot",
  asyncHandler(async (req, res) => {
    const documentId = requireParam(req.params.documentId, "documentId");
    const document = await prisma.document.findFirst({
      where: {
        id: documentId,
        project: { memberships: { some: { userId: req.user!.sub } } }
      }
    });

    if (!document) {
      throw new HttpError(404, "Document not found", "DOCUMENT_NOT_FOUND");
    }

    const ydoc = new Y.Doc();
    const text = ydoc.getText("code");
    if (document.yState) {
      Y.applyUpdate(ydoc, new Uint8Array(document.yState));
    } else {
      text.insert(0, document.plainText);
    }
    const update = Y.encodeStateAsUpdate(ydoc);

    res.json({
      documentId: document.id,
      version: document.version,
      stateVector: Buffer.from(Y.encodeStateVector(ydoc)).toString("base64"),
      update: Buffer.from(update).toString("base64")
    });
  })
);
